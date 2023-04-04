import os
import sys

from typing import Tuple, Union

import faster_whisper
import whisper

from tqdm import tqdm

from tafrigh.config import Config
from tafrigh.recognizer import Recognizer
from tafrigh.transcript_writer import TranscriptWriter
from tafrigh.utils import cli_utils
from tafrigh.utils import whisper_utils
from tafrigh.youtube_downloader import YoutubeDownloader


def main():
    args = cli_utils.parse_args(sys.argv[1:])

    config = Config(
        urls=args.urls,
        model_name_or_ct2_model_path=args.model_name_or_ct2_model_path,
        wit_client_access_token=args.wit_client_access_token,
        task=args.task,
        language=args.language,
        beam_size=args.beam_size,
        ct2_compute_type=args.ct2_compute_type,
        min_words_per_segment=args.min_words_per_segment,
        output_formats=args.output_formats,
        save_yt_dlp_responses=args.save_yt_dlp_responses,
        output_dir=args.output_dir,
        verbose=args.verbose,
    )

    farrigh(config)


def farrigh(config: Config) -> None:
    prepare_output_dir(config.output.output_dir)

    model = None

    if not config.use_wit():
        model, config.whisper.language = whisper_utils.load_model(config.whisper)

    for url in tqdm(config.input.urls, desc='URLs'):
        process_url(url, model, config)


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_url(
    url: str,
    model: Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel], str],
    config: Config,
) -> None:
    url_data = YoutubeDownloader(output_dir=config.output.output_dir).download(
        url,
        save_response=config.output.save_yt_dlp_responses,
    )

    if '_type' in url_data and url_data['_type'] == 'playlist':
        url_data = url_data['entries']
    else:
        url_data = [url_data]

    for element in tqdm(url_data, desc='URL elements'):
        if not element:
            continue

        file_path = os.path.join(config.output.output_dir, f"{element['id']}.wav")

        recognizer = Recognizer(verbose=config.input.verbose)
        if config.use_wit():
            segments = recognizer.recognize_wit(file_path, config.wit)
        else:
            segments = recognizer.recognize_whisper(file_path, model, config.whisper)

        transcript_writer = TranscriptWriter()

        for output_format in config.output.output_formats:
            transcript_writer.write(
                output_format,
                os.path.join(config.output.output_dir, f"{element['id']}.{output_format}"),
                segments,
                config.output.min_words_per_segment,
            )
