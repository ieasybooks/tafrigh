import os
import logging

from typing import Any, Dict, List, Tuple, Union

import faster_whisper
import stable_whisper
import whisper

from tqdm import tqdm


def load_model(
    model_name_or_ct2_model_path: str,
    language: str,
    ct2_compute_type: str,
) -> Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel], str]:
    if model_name_or_ct2_model_path in whisper.available_models():
        if model_name_or_ct2_model_path.endswith('.en'):
            logging.warn(f'{model_name_or_ct2_model_path} is an English-only model, setting language to English.')
            language = 'en'

        return stable_whisper.load_model(model_name_or_ct2_model_path), language
    else:
        return faster_whisper.WhisperModel(model_name_or_ct2_model_path, compute_type=ct2_compute_type), language
