from typing import TypeVar

import faster_whisper
import whisper


WhisperModel = TypeVar(
    'WhisperModel',
    whisper.Whisper,
    faster_whisper.WhisperModel,
)
