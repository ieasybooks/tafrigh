import logging

from typing import List

from tafrigh.types.transcript_type import TranscriptType


class Config:
    def __init__(
        self,
        urls: List[str],
        verbose: bool,
        model_name_or_ct2_model_path: str,
        task: str,
        language: str,
        use_jax: bool,
        beam_size: int,
        ct2_compute_type: str,
        wit_client_access_token: str,
        max_cutting_duration: int,
        min_words_per_segment: int,
        save_files_before_compact: bool,
        save_yt_dlp_responses: bool,
        output_sample: int,
        output_formats: List[str],
        output_dir: str,
    ):
        self.input = self.Input(urls, verbose)
        self.whisper = self.Whisper(model_name_or_ct2_model_path, task, language, use_jax, beam_size, ct2_compute_type)
        self.wit = self.Wit(wit_client_access_token, max_cutting_duration)

        self.output = self.Output(
            min_words_per_segment,
            save_files_before_compact,
            save_yt_dlp_responses,
            output_sample,
            output_formats,
            output_dir,
        )

    def use_wit(self) -> bool:
        return self.wit.wit_client_access_token != ''

    class Input:
        def __init__(self, urls: List[str], verbose: bool):
            self.urls = urls
            self.verbose = verbose

    class Whisper:
        def __init__(
            self,
            model_name_or_ct2_model_path: str,
            task: str,
            language: str,
            use_jax: bool,
            beam_size: int,
            ct2_compute_type: str,
        ):
            if model_name_or_ct2_model_path.endswith('.en'):
                logging.warn(f'{model_name_or_ct2_model_path} is an English-only model, setting language to English.')
                language = 'en'

            self.model_name_or_ct2_model_path = model_name_or_ct2_model_path
            self.task = task
            self.language = language
            self.use_jax = use_jax
            self.beam_size = beam_size
            self.ct2_compute_type = ct2_compute_type

    class Wit:
        def __init__(self, wit_client_access_token: str, max_cutting_duration: int):
            self.wit_client_access_token = wit_client_access_token
            self.max_cutting_duration = max_cutting_duration

    class Output:
        def __init__(
            self,
            min_words_per_segment: int,
            save_files_before_compact: bool,
            save_yt_dlp_responses: bool,
            output_sample: int,
            output_formats: List[str],
            output_dir: str,
        ):
            if 'all' in output_formats:
                output_formats = list(TranscriptType)
            else:
                output_formats = [TranscriptType(output_format) for output_format in output_formats]

            if TranscriptType.ALL in output_formats:
                output_formats.remove(TranscriptType.ALL)

            if TranscriptType.NONE in output_formats:
                output_formats.remove(TranscriptType.NONE)

            self.min_words_per_segment = min_words_per_segment
            self.save_files_before_compact = save_files_before_compact
            self.save_yt_dlp_responses = save_yt_dlp_responses
            self.output_sample = output_sample
            self.output_formats = output_formats
            self.output_dir = output_dir
