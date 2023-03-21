import json
import os
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


def main() -> None:
    args = cli_utils.parse_args()

    prepare_output_dir(args.output_dir)
    model, args.language = whisper_utils.load_model(args.model, args.language)

    for url in args.urls:
        url_data = process_url(url, args.output_dir, args.save_yt_dlp_responses)

        for element in url_data:
            process_file(
                element,
                model,
                args.task,
                args.language,
                args.output_dir,
                args.format,
                args.save_yt_dlp_responses,
                args.verbose,
            )


def prepare_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)


def process_url(url: str, output_dir: str, save_yt_dlp_responses: bool) -> List[Dict[str, Any]]:
    url_data = yt_dlp_utils.download_and_get_url_data(url, output_dir)

    if '_type' in url_data and url_data['_type'] == 'playlist':
        if save_yt_dlp_responses:
            with open(os.path.join(output_dir, f"{url_data['id']}.json"), 'w') as fp:
                json.dump(url_data, fp, indent=4, ensure_ascii=False)

        return url_data['entries']
    else:
        return [url_data]


def process_file(
    url_data: Dict[str, Any],
    model: whisper.Whisper,
    task: str,
    language: str,
    output_dir: str,
    format: TranscriptType,
    save_yt_dlp_responses: bool,
    verbose: bool,
) -> None:
    warnings.filterwarnings('ignore')
    result = whisper_utils.transcript_audio(f"{url_data['id']}.mp3", model, task, language, output_dir, verbose)
    warnings.filterwarnings('default')

    with open(os.path.join(output_dir, f"{url_data['id']}.{format}"), 'w', encoding='utf-8') as fp:
        TRANSCRIPT_WRITE_FUNC[format](result['segments'], file=fp)

    with open(os.path.join(output_dir, f"{url_data['id']}.txt"), 'w', encoding='utf-8') as fp:
        fp.write(result['text'])

    if save_yt_dlp_responses:
        with open(os.path.join(output_dir, f"{url_data['id']}.json"), 'w', encoding='utf-8') as fp:
            json.dump(url_data, fp, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
