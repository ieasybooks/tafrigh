import os
import logging

from typing import Any, Dict, List, Tuple, Union

import faster_whisper
import whisper


def load_model(
    model_name_or_ct2_model_path: str,
    language: str,
    ct2_compute_type: str,
) -> Tuple[Union[whisper.Whisper, faster_whisper.WhisperModel], str]:
    if model_name_or_ct2_model_path in whisper.available_models():
        if model_name_or_ct2_model_path.endswith('.en'):
            logging.warn(f'{model_name_or_ct2_model_path} is an English-only model, setting language to English.')
            language = 'en'

        return whisper.load_model(model_name_or_ct2_model_path), language
    else:
        return faster_whisper.WhisperModel(model_name_or_ct2_model_path, compute_type=ct2_compute_type), language


def transcript_audio(
    audio_file_path: str,
    model: Union[whisper.Whisper, faster_whisper.WhisperModel],
    task: str,
    language: str,
    output_dir: str,
    verbose: bool,
) -> List[Dict[str, Any]]:
    if type(model) is whisper.Whisper:
        segments = model.transcribe(
            audio=os.path.join(output_dir, audio_file_path),
            verbose=verbose,
            **{
                'task': task,
                'language': language,
            },
        )['segments']
    elif type(model) is faster_whisper.WhisperModel:
        segments = model.transcribe(
            audio=os.path.join(output_dir, audio_file_path),
            task=task,
            language=language,
        )[0]

        segments = list(map(lambda segment: {
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
        }, segments))

    return segments
