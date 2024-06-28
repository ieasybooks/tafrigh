__all__ = [
  'farrigh',
  'Config',
  'Downloader',
  'TranscriptType',
  'Writer',
  'WhisperRecognizer',
  'AudioSplitter',
  'WitRecognizer',
]


from .cli import farrigh
from .config import Config
from .downloader import Downloader
from .types.transcript_type import TranscriptType
from .writer import Writer


try:
  from .recognizers.whisper_recognizer import WhisperRecognizer
except ModuleNotFoundError:
  pass

try:
  from .audio_splitter import AudioSplitter
  from .recognizers.wit_recognizer import WitRecognizer
except ModuleNotFoundError:
  pass
