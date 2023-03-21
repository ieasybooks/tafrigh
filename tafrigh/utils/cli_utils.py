
import argparse

import whisper

from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE

from tafrigh.types.transcript_type import TranscriptType


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('urls', nargs='+', type=str, help='Video/Playlist URLs to transcribe.')

    parser.add_argument(
        '-m',
        '--model',
        default='small',
        choices=whisper.available_models(),
        help='Name of the Whisper model to use.',
    )

    parser.add_argument(
        '-t',
        '--task',
        type=str,
        default='transcribe',
        choices=[
            'transcribe',
            'translate',
        ],
        help="Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').",
    )

    parser.add_argument(
        '-l',
        '--language',
        type=str,
        default=None,
        choices=sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
        help='Language spoken in the audio, skip to perform language detection.',
    )

    parser.add_argument(
        '-f',
        '--format',
        default=TranscriptType.SRT,
        choices=list(TranscriptType),
        type=TranscriptType,
        help='Transcript format to output, pass none to skip writing transcripts.',
    )

    parser.add_argument(
        '--output_txt_file',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Whether to produce a text file or not.',
    )

    parser.add_argument(
        '--save_yt_dlp_responses',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to save the yt-dlp library JSON responses or not.',
    )

    parser.add_argument('-o', '--output_dir', type=str, default='.', help='Directory to save the outputs.')

    parser.add_argument(
        '--verbose',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to print out the progress and debug messages.',
    )

    return parser.parse_args()
