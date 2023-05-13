from typing import TypeVar

import faster_whisper
import whisper
import whisper_jax


WhisperModel = TypeVar(
    'WhisperModel',
    whisper.Whisper,
    faster_whisper.WhisperModel,
    whisper_jax.FlaxWhisperPipline,
)
