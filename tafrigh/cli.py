import csv
import logging
import os
import random
import re
import sys

from collections import deque
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple, Union

from tqdm import tqdm

from tafrigh.config import Config
from tafrigh.downloader import Downloader
from tafrigh.utils import cli_utils
from tafrigh.utils import file_utils
from tafrigh.utils import time_utils
from tafrigh.writer import Writer

try:
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

    deque(farrigh(config), maxlen=0)


def farrigh(config: Config) -> Generator[Dict[str, int], None, None]:
    prepare_output_dir(config.output.output_dir)

    model = None
    if not config.use_wit():
        model = whisper_utils.load_model(config.whisper)

    segments = []

    for idx, item in enumerate(tqdm(config.input.urls_or_paths, desc='URLs or local paths')):
        progress_info = {'outer_total': len(config.input.urls_or_paths), 'outer_current': idx + 1}

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
            continue

    write_output_sample(segments, config.output)


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_local(
    path: Path,
    model: 'WhisperModel',
    config: Config,
    progress_info: dict,
) -> Generator[Tuple[Dict[str, int], List[List[Dict[str, Union[str, float]]]]], None, None]:
    filtered_media_files: List[Path] = file_utils.filter_media_files([path] if path.is_file() else path.iterdir())
    files: List[Dict[str, Any]] = [{'file_name': file.name, 'file_path': file} for file in filtered_media_files]

    for idx, file in enumerate(tqdm(files, desc='Local files')):
        new_progress_info = progress_info.copy()
        new_progress_info.update({'inner_total': len(files), 'inner_current': idx + 1, 'status': 'processing'})
        yield new_progress_info, []

        file_path = str(file['file_path'].absolute())

        if config.use_wit():
            wav_file_path = str(wit_file_utils.convert_to_wav(file['file_path']).absolute())
            segments = WitRecognizer(verbose=config.input.verbose).recognize(wav_file_path, config.wit)

            if file['file_path'].suffix != '.wav':
                Path(wav_file_path).unlink(missing_ok=True)
        else:
            segments = WhisperRecognizer(verbose=config.input.verbose).recognize(file_path, model, config.whisper)

        writer = Writer()
        writer.write_all(Path(file['file_name']).stem, segments, config.output)

        for segment in segments:
            segment['url'] = f"file://{file_path}&t={int(segment['start'])}"
            segment['file_path'] = file_path

        new_progress_info['status'] = 'completed'
        yield new_progress_info, writer.compact_segments(segments, config.output.min_words_per_segment)


def process_url(
    url: str,
    model: 'WhisperModel',
    config: Config,
    progress_info: dict,
) -> Generator[Tuple[Dict[str, int], List[List[Dict[str, Union[str, float]]]]], None, None]:
    url_data = Downloader(output_dir=config.output.output_dir).download(
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
        new_progress_info.update({'inner_total': len(url_data), 'inner_current': idx + 1, 'status': 'processing'})
        yield new_progress_info, []

        file_path = os.path.join(config.output.output_dir, f"{element['id']}.wav")

        if config.use_wit():
            segments = WitRecognizer(verbose=config.input.verbose).recognize(file_path, config.wit)
        else:
            segments = WhisperRecognizer(verbose=config.input.verbose).recognize(file_path, model, config.whisper)

        writer = Writer()
        writer.write_all(element['id'], segments, config.output)

        for segment in segments:
            segment['url'] = f"https://youtube.com/watch?v={element['id']}&t={int(segment['start'])}"
            segment['file_path'] = file_path

        new_progress_info['status'] = 'completed'
        yield new_progress_info, writer.compact_segments(segments, config.output.min_words_per_segment)


def write_output_sample(segments: List[Dict[str, Union[str, float]]], output: Config.Output) -> None:
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
