from typing import Tuple, TypeVar, Union

import faster_whisper
import whisper
import whisper_jax


# Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel, whisper_jax.FlaxWhisperPipline], str]
WhisperModel = TypeVar('WhisperModel', whisper.Whisper, faster_whisper.WhisperModel, whisper_jax.FlaxWhisperPipline)
WhisperModelTuple = Tuple[Union[WhisperModel, WhisperModel, WhisperModel], str]