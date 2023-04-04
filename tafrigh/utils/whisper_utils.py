import logging

from typing import Tuple, Union

import faster_whisper
import stable_whisper
import whisper

from tafrigh.config import Config


def load_model(whisper_config: Config.Whisper) -> Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel], str]:
    if whisper_config.model_name_or_ct2_model_path in whisper.available_models():
        if whisper_config.model_name_or_ct2_model_path.endswith('.en'):
            logging.warn(
                f'{whisper_config.model_name_or_ct2_model_path} is an English-only model, setting language to English.')
            whisper_config.language = 'en'

        return stable_whisper.load_model(whisper_config.model_name_or_ct2_model_path), whisper_config.language
    else:
        return (
            faster_whisper.WhisperModel(
                whisper_config.model_name_or_ct2_model_path,
                compute_type=whisper_config.ct2_compute_type
            ),
            whisper_config.language,
        )
