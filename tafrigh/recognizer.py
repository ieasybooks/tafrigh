import json
import logging
import os
import requests
import tempfile
import warnings

from typing import Dict, List, Union

import faster_whisper
import whisper

from tqdm import tqdm

from tafrigh.audio_splitter import AudioSplitter


class Recognizer:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def recognize_whisper(
        self,
        file_path: str,
        model: Union[whisper.Whisper, faster_whisper.WhisperModel],
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Union[str, int]]]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            if isinstance(model, whisper.Whisper):
                return self._recognize_stable_whisper(
                    file_path,
                    model,
                    task,
                    language,
                    beam_size,
                )
            elif isinstance(model, faster_whisper.WhisperModel):
                return self._recognize_faster_whisper(
                    file_path,
                    model,
                    task,
                    language,
                    beam_size,
                )

    def recognize_wit(self, file_path: str, wit_client_access_token: str) -> List[Dict[str, Union[str, int]]]:
        segments = AudioSplitter().split(file_path, tempfile.gettempdir(), expand_segments_with_noise=True)

        transcriptions = []
        for segment_file_path, start, end in tqdm(segments):
            with open(segment_file_path, 'rb') as wav_file:
                audio_content = wav_file.read()

            response = requests.post(
                'https://api.wit.ai/speech',
                headers={
                    'Authorization': f'Bearer {wit_client_access_token}',
                    'Content-Type': 'audio/wav',
                },
                data=audio_content,
            )

            os.remove(segment_file_path)

            if response.status_code == 200:
                transcriptions.append({
                    'start': start,
                    'end': end,
                    'text': json.loads(response.text.split('\r\n')[-1])['text'],
                })
            else:
                logging.warn(f'Error in requesting wit.ai API: {response.status_code}.')

        return transcriptions

    def _recognize_stable_whisper(
        self,
        audio_file_path: str,
        model: whisper.Whisper,
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Union[str, int]]]:
        segments = model.transcribe(
            audio=audio_file_path,
            verbose=self.verbose,
            task=task,
            language=language,
            beam_size=beam_size,
        ).segments

        return [
            {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
            }
            for segment in segments
        ]

    def _recognize_faster_whisper(
        self,
        audio_file_path: str,
        model: faster_whisper.WhisperModel,
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Union[str, int]]]:
        segments, info = model.transcribe(
            audio=audio_file_path,
            task=task,
            language=language,
            beam_size=beam_size,
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
                    'text': segment.text,
                })

                pbar_update = min(segment.end - last_end, info.duration - pbar.n)
                pbar.update(pbar_update)
                last_end = segment.end

        return converted_segments
