import csv
import logging
import os
import random
import re
import sys

from collections import deque
from pathlib import Path
from typing import Any, Generator, Union

from tqdm import tqdm

from tafrigh.config import Config
from tafrigh.downloader import Downloader
from tafrigh.utils import cli_utils, file_utils, time_utils
from tafrigh.writer import Writer


try:
    import requests

    from tafrigh.recognizers.wit_recognizer import WitRecognizer
    from tafrigh.utils.wit import file_utils as wit_file_utils
except ModuleNotFoundError:
    pass

try:
    from tafrigh.recognizers.whisper_recognizer import WhisperRecognizer
    from tafrigh.types.whisper.type_hints import WhisperModel
    from tafrigh.utils.whisper import whisper_utils
except ModuleNotFoundError:
    pass


def main():
    args = cli_utils.parse_args(sys.argv[1:])

    config = Config(
        urls_or_paths=args.urls_or_paths,
        skip_if_output_exist=args.skip_if_output_exist,
        playlist_items=args.playlist_items,
        verbose=args.verbose,
        #
        model_name_or_path=args.model_name_or_path,
        task=args.task,
        language=args.language,
        use_faster_whisper=args.use_faster_whisper,
        beam_size=args.beam_size,
        ct2_compute_type=args.ct2_compute_type,
        #
        wit_client_access_tokens=args.wit_client_access_tokens,
        max_cutting_duration=args.max_cutting_duration,
        min_words_per_segment=args.min_words_per_segment,
        #
        save_files_before_compact=args.save_files_before_compact,
        save_yt_dlp_responses=args.save_yt_dlp_responses,
        output_sample=args.output_sample,
        output_formats=args.output_formats,
        output_dir=args.output_dir,
    )

    if config.use_wit() and config.input.skip_if_output_exist:
        retries = 3

        while retries > 0:
            try:
                deque(farrigh(config), maxlen=0)
                break
            except requests.exceptions.RetryError:
                retries -= 1
    else:
        deque(farrigh(config), maxlen=0)


def farrigh(config: Config) -> Generator[dict[str, int], None, None]:
    prepare_output_dir(config.output.output_dir)

    model = None
    if not config.use_wit():
        model = whisper_utils.load_model(config.whisper)

    segments = []

    for idx, item in enumerate(tqdm(config.input.urls_or_paths, desc='URLs or local paths')):
        progress_info = {
            'outer_total': len(config.input.urls_or_paths),
            'outer_current': idx + 1,
            'outer_status': 'processing',
        }

        if Path(item).exists():
            file_or_folder = Path(item)
            for progress_info, local_elements_segments in process_local(file_or_folder, model, config, progress_info):
                segments.extend(local_elements_segments)
                yield progress_info
        elif re.match('(https?://)', item):
            for progress_info, url_elements_segments in process_url(item, model, config, progress_info):
                segments.extend(url_elements_segments)
                yield progress_info
        else:
            logging.error(f'Path {item} does not exist and is not a URL either.')

            progress_info['outer_status'] = 'completed'
            yield progress_info

            continue

        progress_info['outer_status'] = 'completed'
        yield progress_info

    write_output_sample(segments, config.output)


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_local(
    path: Path,
    model: 'WhisperModel',
    config: Config,
    progress_info: dict,
) -> Generator[tuple[dict[str, int], list[list[dict[str, Union[str, float]]]]], None, None]:
    filtered_media_files: list[Path] = file_utils.filter_media_files([path] if path.is_file() else path.iterdir())
    files: list[dict[str, Any]] = [{'file_name': file.name, 'file_path': file} for file in filtered_media_files]

    for idx, file in enumerate(tqdm(files, desc='Local files')):
        new_progress_info = progress_info.copy()
        new_progress_info.update(
            {
                'inner_total': len(files),
                'inner_current': idx + 1,
                'inner_status': 'processing',
                'progress': 0.0,
                'remaining_time': None,
            }
        )
        yield new_progress_info, []

        writer = Writer()
        if config.input.skip_if_output_exist and writer.is_output_exist(Path(file['file_name']).stem, config.output):
            new_progress_info['inner_status'] = 'completed'
            yield new_progress_info, []

            continue

        file_path = str(file['file_path'].absolute())

        if config.use_wit():
            wav_file_path = str(wit_file_utils.convert_to_wav(file['file_path']).absolute())
            recognize_generator = WitRecognizer(verbose=config.input.verbose).recognize(wav_file_path, config.wit)
        else:
            recognize_generator = WhisperRecognizer(verbose=config.input.verbose).recognize(
                file_path,
                model,
                config.whisper,
            )

        while True:
            try:
                new_progress_info.update(next(recognize_generator))
                yield new_progress_info, []
            except StopIteration as exception:
                segments = exception.value
                break

        if config.use_wit() and file['file_path'].suffix != '.wav':
            Path(wav_file_path).unlink(missing_ok=True)

        writer.write_all(Path(file['file_name']).stem, segments, config.output)

        for segment in segments:
            segment['url'] = f"file://{file_path}&t={int(segment['start'])}"
            segment['file_path'] = file_path

        new_progress_info['inner_status'] = 'completed'
        new_progress_info['progress'] = 100.0
        yield new_progress_info, writer.compact_segments(segments, config.output.min_words_per_segment)


def process_url(
    url: str,
    model: 'WhisperModel',
    config: Config,
    progress_info: dict,
) -> Generator[tuple[dict[str, int], list[list[dict[str, Union[str, float]]]]], None, None]:
    url_data = Downloader(playlist_items=config.input.playlist_items, output_dir=config.output.output_dir).download(
        url,
        save_response=config.output.save_yt_dlp_responses,
    )

    if '_type' in url_data and url_data['_type'] == 'playlist':
        url_data = url_data['entries']
    else:
        url_data = [url_data]

    for idx, element in enumerate(tqdm(url_data, desc='URL elements')):
        if not element:
            continue

        new_progress_info = progress_info.copy()
        new_progress_info.update(
            {
                'inner_total': len(url_data),
                'inner_current': idx + 1,
                'inner_status': 'processing',
                'progress': 0.0,
                'remaining_time': None,
            }
        )
        yield new_progress_info, []

        writer = Writer()
        if config.input.skip_if_output_exist and writer.is_output_exist(element['id'], config.output):
            new_progress_info['inner_status'] = 'completed'
            yield new_progress_info, []

            continue

        file_path = os.path.join(config.output.output_dir, f"{element['id']}.wav")

        if config.use_wit():
            recognize_generator = WitRecognizer(verbose=config.input.verbose).recognize(file_path, config.wit)
        else:
            recognize_generator = WhisperRecognizer(verbose=config.input.verbose).recognize(
                file_path,
                model,
                config.whisper,
            )

        while True:
            try:
                new_progress_info.update(next(recognize_generator))
                yield new_progress_info, []
            except StopIteration as exception:
                segments = exception.value
                break

        writer.write_all(element['id'], segments, config.output)

        for segment in segments:
            segment['url'] = f"https://youtube.com/watch?v={element['id']}&t={int(segment['start'])}"
            segment['file_path'] = file_path

        new_progress_info['inner_status'] = 'completed'
        new_progress_info['progress'] = 100.0
        yield new_progress_info, writer.compact_segments(segments, config.output.min_words_per_segment)


def write_output_sample(segments: list[dict[str, Union[str, float]]], output: Config.Output) -> None:
    if output.output_sample == 0:
        return

    random.shuffle(segments)

    with open(os.path.join(output.output_dir, 'sample.csv'), 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=['start', 'end', 'text', 'url', 'file_path'])
        writer.writeheader()

        for segment in segments[: output.output_sample]:
            segment['start'] = time_utils.format_timestamp(segment['start'], include_hours=True, decimal_marker=',')
            segment['end'] = time_utils.format_timestamp(segment['end'], include_hours=True, decimal_marker=',')
            writer.writerow(segment)
