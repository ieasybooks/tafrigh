import json
import os
import sys
import warnings

from typing import Any, Dict, List

import whisper

from tafrigh.types.transcript_type import TranscriptType

from tafrigh.utils import cli_utils
from tafrigh.utils import transcript_utils
from tafrigh.utils import whisper_utils
from tafrigh.utils import yt_dlp_utils


TRANSCRIPT_WRITE_FUNC = {
    TranscriptType.VTT: transcript_utils.write_vtt,
    TranscriptType.SRT: transcript_utils.write_srt,
}


def main(argv: List[str]) -> None:
    args = cli_utils.parse_args(argv)

    prepare_output_dir(args.output_dir)
    model, args.language = whisper_utils.load_model(
        args.model_name_or_ct2_model_path,
        args.language,
        args.ct2_compute_type,
    )

    for url in args.urls:
        url_data = process_url(url, args.save_yt_dlp_responses, args.output_dir)

        for element in url_data:
            segments = process_file(
                element,
                model,
                args.task,
                args.language,
                args.beam_size,
                args.output_dir,
                args.verbose,
            )

            segments = compact_segments(segments, args.min_words_per_segment)

            write_outputs(
                element,
                segments,
                args.format,
                args.output_txt_file,
                args.output_dir,
            )


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


def process_file(
    url_data: Dict[str, Any],
    model: whisper.Whisper,
    task: str,
    language: str,
    beam_size: int,
    output_dir: str,
    verbose: bool,
) -> List[Dict[str, Any]]:
    warnings.filterwarnings('ignore')
    segments = whisper_utils.transcript_audio(
        f"{url_data['id']}.m4a",
        model,
        task,
        language,
        beam_size,
        output_dir,
        verbose,
    )
    warnings.filterwarnings('default')

    return segments


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


def write_outputs(
    url_data: Dict[str, Any],
    segments: List[Dict[str, Any]],
    format: TranscriptType,
    output_txt_file: bool,
    output_dir: str,
) -> None:
    if format != TranscriptType.NONE:
        with open(os.path.join(output_dir, f"{url_data['id']}.{format}"), 'w', encoding='utf-8') as fp:
            TRANSCRIPT_WRITE_FUNC[format](segments, file=fp)

    if output_txt_file:
        with open(os.path.join(output_dir, f"{url_data['id']}.txt"), 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(list(map(lambda segment: segment['text'].strip(), segments))))
            fp.write('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
