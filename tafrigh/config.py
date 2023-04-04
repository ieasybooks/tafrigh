from typing import List

from tafrigh.types.transcript_type import TranscriptType


class Config:
    def __init__(
        self,
        urls: List[str],
        model_name_or_ct2_model_path: str,
        wit_client_access_token: str,
        task: str,
        language: str,
        beam_size: int,
        ct2_compute_type: str,
        min_words_per_segment: int,
        output_formats: List[str],
        save_yt_dlp_responses: bool,
        output_dir: str,
        verbose: bool,
    ):
        self.input = self.Input(urls, verbose)
        self.whisper = self.Whisper(model_name_or_ct2_model_path, task, language, beam_size, ct2_compute_type)
        self.wit = self.Wit(wit_client_access_token)
        self.output = self.Output(min_words_per_segment, output_formats, save_yt_dlp_responses, output_dir)

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
            beam_size: int,
            ct2_compute_type: str,
        ):
            self.model_name_or_ct2_model_path = model_name_or_ct2_model_path
            self.task = task
            self.language = language
            self.beam_size = beam_size
            self.ct2_compute_type = ct2_compute_type

    class Wit:
        def __init__(self, wit_client_access_token: str):
            self.wit_client_access_token = wit_client_access_token

    class Output:
        def __init__(
            self,
            min_words_per_segment: int,
            output_formats: List[str],
            save_yt_dlp_responses: bool,
            output_dir: str,
        ):
            if 'all' in output_formats:
                output_formats = list(TranscriptType)
            else:
                output_formats = [TranscriptType(output_format) for output_format in output_formats]

            output_formats.remove(TranscriptType.ALL)
            output_formats.remove(TranscriptType.NONE)

            self.output_dir = output_dir
            self.min_words_per_segment = min_words_per_segment
            self.output_formats = output_formats
            self.save_yt_dlp_responses = save_yt_dlp_responses
