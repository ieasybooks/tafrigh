import json
import logging
import multiprocessing
import os
import shutil
import tempfile
import time
from typing import Generator, Union

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from tafrigh.audio_splitter import AudioSplitter
from tafrigh.config import Config
from tafrigh.utils.decorators import minimum_execution_time


class WitRecognizer:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def recognize(
        self,
        file_path: str,
        wit_config: Config.Wit,
    ) -> Generator[dict[str, float], None, list[dict[str, Union[str, float]]]]:

        temp_directory = tempfile.mkdtemp()

        segments = AudioSplitter().split(
            file_path,
            temp_directory,
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

        with multiprocessing.Pool(processes=min(4, multiprocessing.cpu_count() - 1)) as pool:
            async_results = [
                pool.apply_async(self._process_segment, (segment, file_path, wit_config, session))
                for segment in segments
            ]

            transcriptions = []

            with tqdm(total=len(segments), disable=self.verbose is not False) as pbar:
                while async_results:
                    if async_results[0].ready():
                        transcriptions.append(async_results.pop(0).get())
                        pbar.update(1)

                    yield {
                        'progress': round(len(transcriptions) / len(segments) * 100, 2),
                        'remaining_time': (pbar.total - pbar.n) / pbar.format_dict['rate'] if pbar.format_dict['rate'] and pbar.total else None,
                    }

                    time.sleep(0.5)

        shutil.rmtree(temp_directory)

        return transcriptions

    @minimum_execution_time(min(4, multiprocessing.cpu_count() - 1) + 1)
    def _process_segment(
        self,
        segment: tuple[str, float, float],
        file_path: str,
        wit_config: Config.Wit,
        session: requests.Session,
    ) -> dict[str, Union[str, float]]:
        segment_file_path, start, end = segment

        with open(segment_file_path, 'rb') as wav_file:
            audio_content = wav_file.read()

        retries = 5

        text = ''
        while retries > 0:
            response = session.post(
                'https://api.wit.ai/speech',
                headers={
                    'Accept': 'application/vnd.wit.20200513+json',
                    'Content-Type': 'audio/wav',
                    'Authorization': f'Bearer {wit_config.wit_client_access_token}',
                },
                data=audio_content,
            )

            if response.status_code == 200:
                try:
                    text = json.loads(response.text)['text']
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
