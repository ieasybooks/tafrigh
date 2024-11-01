import logging

import requests

from .types.transcript_type import TranscriptType


class Config:
  def __init__(self, input: 'Config.Input', whisper: 'Config.Whisper', wit: 'Config.Wit', output: 'Config.Output'):
    self.input = input
    self.whisper = whisper
    self.wit = wit
    self.output = output

  def use_wit(self) -> bool:
    return self.wit.wit_client_access_tokens != []

  class Input:
    def __init__(
      self,
      urls_or_paths: list[str],
      skip_if_output_exist: bool,
      download_retries: int,
      yt_dlp_options: str,
      verbose: bool,
    ):
      self.urls_or_paths = urls_or_paths
      self.skip_if_output_exist = skip_if_output_exist
      self.download_retries = download_retries
      self.yt_dlp_options = yt_dlp_options
      self.verbose = verbose

  class Whisper:
    def __init__(
      self,
      model_name_or_path: str,
      task: str,
      language: str,
      use_faster_whisper: bool,
      beam_size: int,
      ct2_compute_type: str,
    ):
      if model_name_or_path.endswith('.en'):
        logging.warn(f'{model_name_or_path} is an English-only model, setting language to English.')
        language = 'en'

      self.model_name_or_path = model_name_or_path
      self.task = task
      self.language = language
      self.use_faster_whisper = use_faster_whisper
      self.beam_size = beam_size
      self.ct2_compute_type = ct2_compute_type

  class Wit:
    def __init__(self, wit_client_access_tokens: list[str] | None, max_cutting_duration: int):
      if wit_client_access_tokens is None:
        self.wit_client_access_tokens = []
        self.language = ''
      else:
        self.wit_client_access_tokens = [key for key in wit_client_access_tokens if key is not None and key != '']
        self.language = self._get_language()

      self.max_cutting_duration = max_cutting_duration

    def _get_language(self) -> str:
      languages = set()

      for wit_client_access_token in self.wit_client_access_tokens:
        applications = requests.get(
          'https://api.wit.ai/apps?limit=10000',
          headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {wit_client_access_token}',
          },
        ).json()

        languages.add(next(filter(lambda app: 'is_app_for_token' in app, applications))['lang'])

      assert len(languages) == 1, 'All Wit.ai client access tokens must be for the same language.'

      return list(languages)[0]

  class Output:
    def __init__(
      self,
      min_words_per_segment: int,
      save_files_before_compact: bool,
      save_yt_dlp_responses: bool,
      output_sample: int,
      output_formats: list[str],
      output_dir: str,
    ):
      if 'all' in output_formats:
        output_formats = [transcript_type.value for transcript_type in TranscriptType]

      if TranscriptType.ALL in output_formats:
        output_formats.remove(str(TranscriptType.ALL))

      if TranscriptType.NONE in output_formats:
        output_formats.remove(str(TranscriptType.NONE))

      self.min_words_per_segment = min_words_per_segment
      self.save_files_before_compact = save_files_before_compact
      self.save_yt_dlp_responses = save_yt_dlp_responses
      self.output_sample = output_sample
      self.output_formats = output_formats
      self.output_dir = output_dir
