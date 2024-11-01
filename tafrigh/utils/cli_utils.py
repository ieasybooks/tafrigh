import argparse
import importlib.metadata
import re

from tafrigh.types.transcript_type import TranscriptType


def parse_args(argv: list[str]) -> argparse.Namespace:
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--version',
    action='version',
    version=importlib.metadata.version('tafrigh'),
  )

  input_group = parser.add_argument_group('Input')

  input_group.add_argument(
    'urls_or_paths',
    nargs='+',
    help='Video/Playlist URLs or local folder/file(s) to transcribe.',
  )

  input_group.add_argument(
    '--skip_if_output_exist',
    action=argparse.BooleanOptionalAction,
    default=False,
    help='Whether to skip generating the output if the output file already exists.',
  )

  input_group.add_argument(
    '--download_retries',
    type=int,
    default=3,
    help="Number of retries for yt-dlp downloads that fail.",
  )

  input_group.add_argument(
    '--yt_dlp_options',
    type=str,
    default='{}',
    help="Additional options to pass to yt-dlp in valid JSON format (e.g. `'{\"playlist_items\": \"1-10\"}'`).",
  )

  input_group.add_argument(
    '--verbose',
    action=argparse.BooleanOptionalAction,
    default=False,
    help='Whether to print out the progress and debug messages.',
  )

  whisper_group = parser.add_argument_group('Whisper')

  whisper_group.add_argument(
    '-m',
    '--model_name_or_path',
    default='small',
    help='Name or path of the Whisper model to use.',
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
    choices=['af', 'am', 'ar', 'as', 'az', 'ba', 'be', 'bg', 'bn', 'bo', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de']
    + ['el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'gl', 'gu', 'ha', 'haw', 'he', 'hi', 'hr', 'ht', 'hu']
    + ['hy', 'id', 'is', 'it', 'ja', 'jw', 'ka', 'kk', 'km', 'kn', 'ko', 'la', 'lb', 'ln', 'lo', 'lt', 'lv', 'mg']
    + ['mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'nn', 'no', 'oc', 'pa', 'pl', 'ps', 'pt', 'ro']
    + ['ru', 'sa', 'sd', 'si', 'sk', 'sl', 'sn', 'so', 'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'tk']
    + ['tl', 'tr', 'tt', 'uk', 'ur', 'uz', 'vi', 'yi', 'yo', 'zh'],
    help='Language spoken in the audio, skip to perform language detection.',
  )

  whisper_group.add_argument(
    '--use_faster_whisper',
    action=argparse.BooleanOptionalAction,
    default=False,
    help='Whether to use Faster Whisper implementation.',
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
    '--wit_client_access_tokens',
    nargs='+',
    help='List of wit.ai client access tokens. If provided, wit.ai APIs will be used to do the transcription, otherwise whisper will be used.',
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


def int_or_none(v, scale=1, default=None, get_attr=None, invscale=1):
  if get_attr and v is not None:
    v = getattr(v, get_attr, None)

  try:
    return int(v) * invscale // scale
  except (ValueError, TypeError, OverflowError):
    return default
