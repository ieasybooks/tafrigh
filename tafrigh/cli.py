import json
import os
import sys

from typing import Any, Dict, List

import tqdm

from tafrigh.recognizer import Recognizer
from tafrigh.transcript_writer import TranscriptWriter
from tafrigh.types.transcript_type import TranscriptType

from tafrigh.utils import cli_utils
from tafrigh.utils import whisper_utils
from tafrigh.utils import yt_dlp_utils


def main():
    args = cli_utils.parse_args(sys.argv[1:])

    farrigh(
        urls=args.urls,
        model_name_or_ct2_model_path=args.model_name_or_ct2_model_path,
        task=args.task,
        language=args.language,
        beam_size=args.beam_size,
        ct2_compute_type=args.ct2_compute_type,
        min_words_per_segment=args.min_words_per_segment,
        format=args.format,
        output_txt_file=args.output_txt_file,
        save_yt_dlp_responses=args.save_yt_dlp_responses,
        output_dir=args.output_dir,
        verbose=args.verbose,
    )


def farrigh(
    urls: List[str],
    model_name_or_ct2_model_path: str,
    task: str,
    language: str,
    beam_size: int,
    ct2_compute_type: str,
    min_words_per_segment: int,
    format: TranscriptType,
    output_txt_file: bool,
    save_yt_dlp_responses: bool,
    output_dir: str,
    verbose: bool,
) -> None:
    prepare_output_dir(output_dir)

    model, language = whisper_utils.load_model(
        model_name_or_ct2_model_path,
        language,
        ct2_compute_type,
    )

    for url in tqdm.tqdm(urls, desc='URLs'):
        url_data = process_url(url, save_yt_dlp_responses, output_dir)

        for element in tqdm.tqdm(url_data, desc='URL elements'):
            recognizer = Recognizer(verbose=verbose)
            segments = recognizer.recognize_whisper(
                os.path.join(output_dir, f"{element['id']}.m4a"),
                model,
                task,
                language,
                beam_size,
            )

            segments = compact_segments(segments, min_words_per_segment)

            transcript_writer = TranscriptWriter()
            transcript_writer.write(format, os.path.join(output_dir, f"{url_data['id']}.{format}"), segments)
            if output_txt_file:
                transcript_writer.write(TranscriptType.TXT, os.path.join(output_dir, f"{url_data['id']}.txt"), segments)


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_url(url: str, save_yt_dlp_responses: bool, output_dir: str) -> List[Dict[str, Any]]:
    return_data = None
    url_data = yt_dlp_utils.download_and_get_url_data(url, output_dir)

    if '_type' in url_data and url_data['_type'] == 'playlist':
        for entry in url_data['entries']:
            for requested_download in entry['requested_downloads']:
                del requested_download['__postprocessors']

        return_data = url_data['entries']
    else:
        for requested_download in url_data['requested_downloads']:
            del requested_download['__postprocessors']

        return_data = [url_data]

    if save_yt_dlp_responses:
        with open(os.path.join(output_dir, f"{url_data['id']}.json"), 'w', encoding='utf-8') as fp:
            json.dump(url_data, fp, indent=4, ensure_ascii=False)

    return return_data


def compact_segments(segments: List[Dict[str, Any]], min_words_per_segment: int) -> List[Dict[str, Any]]:
    if min_words_per_segment == 0:
        return segments

    compacted_segments = list()
    tmp_segment = None

    for segment in segments:
        if tmp_segment:
            tmp_segment['text'] += f" {segment['text'].strip()}"
            tmp_segment['end'] = segment['end']

            if len(tmp_segment['text'].split()) >= min_words_per_segment:
                compacted_segments.append(tmp_segment)
                tmp_segment = None
        elif len(segment['text'].split()) < min_words_per_segment:
            tmp_segment = segment
        elif len(segment['text'].split()) >= min_words_per_segment:
            compacted_segments.append(segment)

    if tmp_segment:
        compacted_segments.append(tmp_segment)

    return compacted_segments


if __name__ == '__main__':
    main()
