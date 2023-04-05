import logging

from typing import Tuple, Union

import faster_whisper
import stable_whisper
import whisper

from tafrigh.config import Config


def load_model(whisper_config: Config.Whisper) -> Union[whisper.Whisper, faster_whisper.WhisperModel]:
    if whisper_config.model_name_or_ct2_model_path in whisper.available_models():
        return stable_whisper.load_model(whisper_config.model_name_or_ct2_model_path)
    else:
        return faster_whisper.WhisperModel(
            whisper_config.model_name_or_ct2_model_path,
            compute_type=whisper_config.ct2_compute_type
        )
