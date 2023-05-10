import argparse

from typing import List

from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE

from tafrigh.types.transcript_type import TranscriptType


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    input_group = parser.add_argument_group('Input')

    input_group.add_argument('urls_or_paths', nargs='+', help='Video/Playlist URLs or local folder/file(s) to transcribe.')

    input_group.add_argument(
        '--verbose',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to print out the progress and debug messages.',
    )

    whisper_group = parser.add_argument_group('Whisper')

    whisper_group.add_argument(
        '-m',
        '--model_name_or_ct2_model_path',
        default='small',
        help='Name of the Whisper model to use or a path to CTranslate2 model converted using `ct2-transformers-converter` tool.',
    )

    whisper_group.add_argument(
        '-t',
        '--task',
        default='transcribe',
        choices=[
            'transcribe',
            'translate',
        ],
        help="Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate').",
    )

    whisper_group.add_argument(
        '-l',
        '--language',
        default=None,
        choices=sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
        help='Language spoken in the audio, skip to perform language detection.',
    )

    whisper_group.add_argument(
        '--use_jax',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to use Whisper JAX implementation. Make sure to have JAX installed before using this option.',
    )

    whisper_group.add_argument(
        '--beam_size',
        type=int,
        default=5,
        help='Number of beams in beam search, only applicable when temperature is zero.',
    )

    whisper_group.add_argument(
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

    wit_group = parser.add_argument_group('Wit')

    wit_group.add_argument(
        '-w',
        '--wit_client_access_token',
        default='',
        help='wit.ai client access token. If provided, wit.ai APIs will be used to do the transcription, otherwise whisper will be used.',
    )

    wit_group.add_argument(
        '--max_cutting_duration',
        type=int,
        default=15,
        choices=range(1, 17),
        metavar='[1-17]',
        help='The maximum allowed cutting duration. It should be between 1 and 17.',
    )

    output_group = parser.add_argument_group('Output')

    output_group.add_argument(
        '--min_words_per_segment',
        type=int,
        default=1,
        help='The minimum number of words should appear in each transcript segment. Any segment have words count less than this threshold will be merged with the next one. Pass 0 to disable this behavior.',
    )

    output_group.add_argument(
        '--save_files_before_compact',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Saves the output files before applying the compact logic that is based on --min_words_per_segment.',
    )

    output_group.add_argument(
        '--save_yt_dlp_responses',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Whether to save the yt-dlp library JSON responses or not.',
    )

    output_group.add_argument(
        '--output_sample',
        type=int,
        default=0,
        help='Samples random compacted segments from the output and generates a CSV file contains the sampled data. Pass 0 to disable this behavior.',
    )

    output_group.add_argument(
        '-f',
        '--output_formats',
        nargs='+',
        default='all',
        choices=[transcript_type.value for transcript_type in TranscriptType],
        help='Format of the output file; if not specified, all available formats will be produced.',
    )

    output_group.add_argument('-o', '--output_dir', default='.', help='Directory to save the outputs.')

    return parser.parse_args(argv)
