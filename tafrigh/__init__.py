from tafrigh.cli import farrigh
from tafrigh.config import Config
from tafrigh.downloader import Downloader
from tafrigh.types.transcript_type import TranscriptType
from tafrigh.writer import Writer


try:
    from tafrigh.recognizers.whisper_recognizer import WhisperRecognizer
except ModuleNotFoundError:
    pass

try:
    from tafrigh.audio_splitter import AudioSplitter
    from tafrigh.recognizers.wit_recognizer import WitRecognizer
except ModuleNotFoundError:
    pass
