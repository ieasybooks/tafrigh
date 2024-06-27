import json
import logging
import multiprocessing
import time

from typing import Generator, cast

import requests

from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from src.audio_splitter import AudioSplitter
from src.config import Config
from src.recognizers.wit_calling_throttle import WitCallingThrottle, WitCallingThrottleManager
from src.types.segment_type import SegmentType


def init_pool(throttle: WitCallingThrottle) -> None:
  global wit_calling_throttle

  wit_calling_throttle = throttle  # type: ignore


class WitRecognizer:
  def __init__(self, verbose: bool):
    self.verbose = verbose
    self.processes_per_wit_client_access_token = min(4, multiprocessing.cpu_count())

  def recognize(
    self,
    file_path: str,
    wit_config: Config.Wit,
  ) -> Generator[dict[str, float], None, list[SegmentType]]:
    segments = AudioSplitter().split(
      file_path,
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

    pool_processes_count = min(
      self.processes_per_wit_client_access_token * len(wit_config.wit_client_access_tokens or []),
      multiprocessing.cpu_count(),
    )

    with WitCallingThrottleManager() as manager:
      wit_calling_throttle = manager.WitCallingThrottle(len(wit_config.wit_client_access_tokens))  # type: ignore

      with multiprocessing.Pool(
        processes=pool_processes_count,
        initializer=init_pool,
        initargs=(wit_calling_throttle,),
      ) as pool:
        async_results = [
          pool.apply_async(
            self._process_segment,
            (
              segment,
              file_path,
              wit_config,
              session,
              index % len(wit_config.wit_client_access_tokens or []),
            ),
          )
          for index, segment in enumerate(segments)
        ]

        transcriptions = []

        with tqdm(total=len(segments), disable=self.verbose is not False) as pbar:
          for async_result in async_results:
            async_result.wait()
            pbar.update(1)

            transcriptions.append(async_result.get())

            yield {
              'progress': round(len(transcriptions) / len(segments) * 100, 2),
              'remaining_time': (pbar.total - pbar.n) / pbar.format_dict['rate']
              if pbar.format_dict['rate'] and pbar.total
              else None,
            }

    return transcriptions

  def _process_segment(
    self,
    segment: tuple[str, float, float],
    file_path: str,
    wit_config: Config.Wit,
    session: requests.Session,
    wit_client_access_token_index: int,
  ) -> SegmentType:
    wit_calling_throttle.throttle(wit_client_access_token_index)  # type: ignore

    data, start, end = segment

    retries = 5

    text = ''
    while retries > 0:
      try:
        response = session.post(
          'https://api.wit.ai/speech',
          headers={
            'Accept': 'application/vnd.wit.20200513+json',
            'Content-Type': 'audio/mpeg3',
            'Authorization': f'Bearer {cast(list[str], wit_config.wit_client_access_tokens)[wit_client_access_token_index]}',
          },
          data=data,
        )

        if response.status_code == 200:
          text = json.loads(response.text)['text']
          break
        else:
          retries -= 1
          time.sleep(self.processes_per_wit_client_access_token + 1)
      except Exception:
        retries -= 1
        time.sleep(self.processes_per_wit_client_access_token + 1)

    if retries == 0:
      logging.warn(
        f"The segment from `{file_path}` file that starts at {start} and ends at {end} didn't transcribed successfully."
      )

    return SegmentType(text=text.strip(), start=start, end=end)
