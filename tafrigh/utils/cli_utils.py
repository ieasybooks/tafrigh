
import argparse

import whisper

from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE

from tafrigh.types.transcript_type import TranscriptType


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('urls', nargs='+', help='Video/Playlist URLs to transcribe.')

    parser.add_argument(
        '-m',
        '--model_name_or_ct2_model_path',
        default='small',
        help='Name of the Whisper model to use or a path to CTranslate2 model converted using `ct2-transformers-converter` tool.',
    )

    parser.add_argument(
        '-t',
        '--task',
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

    parser.add_argument('-o', '--output_dir', default='.', help='Directory to save the outputs.')

    parser.add_argument(
        '--ct2_compute_type',
        default='default',
        choices=[
            'default',
            'int8',
            'int8_float16',
            'int16',
            'float16',
        ],
        help='Quantization type applied while converting the model to CTranslate2 format.',
    )

    parser.add_argument(
        '--beam_size',
        type=int,
        default=5,
        help='Number of beams in beam search, only applicable when temperature is zero.',
    )

    parser.add_argument(
        '--verbose',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to print out the progress and debug messages.',
    )

    return parser.parse_args()
