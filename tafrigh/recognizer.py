import json
import logging
import multiprocessing
import os
import requests
import tempfile
import time
import warnings

from itertools import repeat
from requests.adapters import HTTPAdapter
from typing import Dict, List, Tuple, Union
from urllib3.util.retry import Retry

import faster_whisper
import whisper
import whisper_jax

from tqdm import tqdm
from tqdm.contrib import concurrent

from tafrigh.audio_splitter import AudioSplitter
from tafrigh.config import Config
from tafrigh.utils.decorators import minimum_execution_time


class Recognizer:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def recognize_whisper(
        self,
        file_path: str,
        model: Union[whisper.Whisper, faster_whisper.WhisperModel, whisper_jax.FlaxWhisperPipline],
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            if isinstance(model, whisper.Whisper):
                return self._recognize_stable_whisper(file_path, model, whisper_config)
            elif isinstance(model, faster_whisper.WhisperModel):
                return self._recognize_faster_whisper(file_path, model, whisper_config)
            elif isinstance(model, whisper_jax.FlaxWhisperPipline):
                return self._recognize_jax_whisper(file_path, model, whisper_config)

    def recognize_wit(self, file_path: str, wit_config: Config.Wit) -> List[Dict[str, Union[str, float]]]:
        segments = AudioSplitter().split(
            file_path,
            tempfile.gettempdir(),
            max_dur=wit_config.max_cutting_duration,
            expand_segments_with_noise=True,
        )

        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['POST'],
            backoff_factor=1,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session = requests.Session()
        session.mount('https://', adapter)

        return concurrent.process_map(
            self._process_segment_wit,
            segments,
            repeat(file_path),
            repeat(wit_config),
            repeat(session),
            max_workers=min(4, multiprocessing.cpu_count() - 1),
            chunksize=1,
        )

    def _recognize_stable_whisper(
        self,
        audio_file_path: str,
        model: whisper.Whisper,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments = model.transcribe(
            audio=audio_file_path,
            verbose=self.verbose,
            task=whisper_config.task,
            language=whisper_config.language,
            beam_size=whisper_config.beam_size,
        ).segments

        return [
            {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
            }
            for segment in segments
        ]

    def _recognize_faster_whisper(
        self,
        audio_file_path: str,
        model: faster_whisper.WhisperModel,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments, info = model.transcribe(
            audio=audio_file_path,
            task=whisper_config.task,
            language=whisper_config.language,
            beam_size=whisper_config.beam_size,
        )

        converted_segments = []
        last_end = 0
        with tqdm(
            total=round(info.duration, 2),
            unit='sec',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]',
            disable=self.verbose is not False,
        ) as pbar:
            for segment in segments:
                converted_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                })

                pbar_update = min(segment.end - last_end, info.duration - pbar.n)
                pbar.update(pbar_update)
                last_end = segment.end

        return converted_segments

    def _recognize_jax_whisper(
        self,
        audio_file_path: str,
        model: whisper_jax.FlaxWhisperPipline,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments = model(
            audio_file_path,
            task=whisper_config.task,
            language=whisper_config.language,
            return_timestamps=True,
        )['chunks']

        return [
            {
                'start': segment['timestamp'][0],
                'end': segment['timestamp'][1],
                'text': segment['text'].strip(),
            }
            for segment in segments
        ]

    @minimum_execution_time(min(4, multiprocessing.cpu_count() - 1) + 1)
    def _process_segment_wit(
        self,
        segment: Tuple[str, float, float],
        file_path: str,
        wit_config: Config.Wit,
        session: requests.Session,
    ) -> Dict[str, Union[str, float]]:
        segment_file_path, start, end = segment

        with open(segment_file_path, 'rb') as wav_file:
            audio_content = wav_file.read()

        retries = 3

        text = ''
        while retries > 0:
            response = session.post(
                'https://api.wit.ai/speech',
                headers={
                    'Authorization': f'Bearer {wit_config.wit_client_access_token}',
                    'Content-Type': 'audio/wav',
                },
                data=audio_content,
            )

            if response.status_code == 200:
                try:
                    text = json.loads(response.text.split('\r\n')[-1])['text']
                    break
                except KeyError:
                    retries -= 1
            else:
                retries -= 1
                time.sleep(min(4, multiprocessing.cpu_count() - 1) + 1)

        if retries == 0:
            logging.warn(
                f"The segment from `{file_path}` file that starts at {start} and ends at {end} didn't transcribed successfully.")

        os.remove(segment_file_path)

        return {
            'start': start,
            'end': end,
            'text': text.strip(),
        }
