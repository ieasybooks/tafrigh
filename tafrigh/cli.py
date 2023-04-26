import csv
import os
import random
import sys

from typing import Dict, List, Tuple, Union

import faster_whisper
import whisper

from tqdm import tqdm

from tafrigh.config import Config
from tafrigh.downloader import Downloader
from tafrigh.recognizer import Recognizer
from tafrigh.utils import cli_utils
from tafrigh.utils import time_utils
from tafrigh.utils import whisper_utils
from tafrigh.writer import Writer


def main():
    args = cli_utils.parse_args(sys.argv[1:])

    config = Config(
        urls=args.urls,
        verbose=args.verbose,

        model_name_or_ct2_model_path=args.model_name_or_ct2_model_path,
        task=args.task,
        language=args.language,
        use_jax=args.use_jax,
        beam_size=args.beam_size,
        ct2_compute_type=args.ct2_compute_type,

        wit_client_access_token=args.wit_client_access_token,
        max_cutting_duration=args.max_cutting_duration,

        min_words_per_segment=args.min_words_per_segment,
        save_files_before_compact=args.save_files_before_compact,
        save_yt_dlp_responses=args.save_yt_dlp_responses,
        output_sample=args.output_sample,
        output_formats=args.output_formats,
        output_dir=args.output_dir,
    )

    farrigh(config)


def farrigh(config: Config) -> None:
    prepare_output_dir(config.output.output_dir)

    model = None
    if not config.use_wit():
        model = whisper_utils.load_model(config.whisper)

    segments = []

    for url in tqdm(config.input.urls, desc='URLs'):
        url_elements_segments = process_url(url, model, config)

        for url_element_segments in url_elements_segments:
            segments.extend(url_element_segments)

    write_output_sample(segments, config.output)


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_url(
    url: str,
    model: Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel], str],
    config: Config,
) -> List[List[Dict[str, Union[str, float]]]]:
    url_data = Downloader(output_dir=config.output.output_dir).download(
        url,
        save_response=config.output.save_yt_dlp_responses,
    )

    if '_type' in url_data and url_data['_type'] == 'playlist':
        url_data = url_data['entries']
    else:
        url_data = [url_data]

    elements_segments = []

    for element in tqdm(url_data, desc='URL elements'):
        if not element:
            continue

        file_path = os.path.join(config.output.output_dir, f"{element['id']}.wav")

        recognizer = Recognizer(verbose=config.input.verbose)
        if config.use_wit():
            segments = recognizer.recognize_wit(file_path, config.wit)
        else:
            segments = recognizer.recognize_whisper(file_path, model, config.whisper)

        writer = Writer()
        writer.write_all(element['id'], segments, config.output)

        for segment in segments:
            segment['url'] = f"https://youtube.com/watch?v={element['id']}&t={int(segment['start'])}"
            segment['file_path'] = file_path

        elements_segments.append(writer.compact_segments(segments, config.output.min_words_per_segment))

    return elements_segments


def write_output_sample(segments: List[Dict[str, Union[str, float]]], output: Config.Output) -> None:
    if output.output_sample == 0:
        return

    random.shuffle(segments)

    with open(os.path.join(output.output_dir, 'sample.csv'), 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=['start', 'end', 'text', 'url', 'file_path'])
        writer.writeheader()

        for segment in segments[:output.output_sample]:
            segment['start'] = time_utils.format_timestamp(segment['start'], include_hours=True, decimal_marker=',')
            segment['end'] = time_utils.format_timestamp(segment['end'], include_hours=True, decimal_marker=',')
            writer.writerow(segment)
