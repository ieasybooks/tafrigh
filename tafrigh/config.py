import logging

from tafrigh.types.transcript_type import TranscriptType


class Config:
    def __init__(
        self,
        urls_or_paths: list[str],
        skip_if_output_exist: bool,
        playlist_items: str,
        verbose: bool,
        model_name_or_path: str,
        task: str,
        language: str,
        use_faster_whisper: bool,
        beam_size: int,
        ct2_compute_type: str,
        wit_client_access_tokens: list[str],
        max_cutting_duration: int,
        min_words_per_segment: int,
        save_files_before_compact: bool,
        save_yt_dlp_responses: bool,
        output_sample: int,
        output_formats: list[str],
        output_dir: str,
    ):
        self.input = self.Input(urls_or_paths, skip_if_output_exist, playlist_items, verbose)

        self.whisper = self.Whisper(
            model_name_or_path,
            task,
            language,
            use_faster_whisper,
            beam_size,
            ct2_compute_type,
        )

        self.wit = self.Wit(wit_client_access_tokens, max_cutting_duration)

        self.output = self.Output(
            min_words_per_segment,
            save_files_before_compact,
            save_yt_dlp_responses,
            output_sample,
            output_formats,
            output_dir,
        )

    def use_wit(self) -> bool:
        return self.wit.wit_client_access_tokens is not None and self.wit.wit_client_access_tokens != []

    class Input:
        def __init__(self, urls_or_paths: list[str], skip_if_output_exist: bool, playlist_items: str, verbose: bool):
            self.urls_or_paths = urls_or_paths
            self.skip_if_output_exist = skip_if_output_exist
            self.playlist_items = playlist_items
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
        def __init__(self, wit_client_access_tokens: list[str], max_cutting_duration: int):
            if wit_client_access_tokens is None:
                self.wit_client_access_tokens = None
            else:
                self.wit_client_access_tokens = [
                    key for key in wit_client_access_tokens if key is not None and key != ''
                ]

            self.max_cutting_duration = max_cutting_duration

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
