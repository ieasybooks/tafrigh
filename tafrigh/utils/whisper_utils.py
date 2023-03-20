import os

from typing import Any, Dict, Tuple

import whisper
import logging


def load_model(model_name: str, language: str) -> Tuple[whisper.Whisper, str]:
    if model_name.endswith('.en'):
        logging.warn(f'{model_name} is an English-only model, setting language to English.')
        language = 'en'

    return whisper.load_model(model_name), language


def transcript_audio(
    audio_file_path: str,
    model: whisper.Whisper,
    task: str,
    language: str,
    output_dir: str,
    verbose: bool,
) -> Dict[str, Any]:
    return model.transcribe(
        audio=os.path.join(output_dir, audio_file_path),
        verbose=verbose,
        **{
            'task': task,
            'language': language,
        },
    )
