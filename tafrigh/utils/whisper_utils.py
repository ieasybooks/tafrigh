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


def transcript_audio(
    audio_file_path: str,
    model: Union[whisper.Whisper, faster_whisper.WhisperModel],
    task: str,
    language: str,
    beam_size: int,
    output_dir: str,
    verbose: bool,
) -> List[Dict[str, Any]]:
    if type(model) is whisper.Whisper:
        return transcript_stable_whisper(
            audio_file_path,
            model,
            task,
            language,
            beam_size,
            output_dir,
            verbose,
        )
    elif type(model) is faster_whisper.WhisperModel:
        return transcript_faster_whisper(
            audio_file_path,
            model,
            task,
            language,
            beam_size,
            output_dir,
            verbose,
        )


def transcript_stable_whisper(
    audio_file_path: str,
    model: Union[whisper.Whisper, faster_whisper.WhisperModel],
    task: str,
    language: str,
    beam_size: int,
    output_dir: str,
    verbose: bool,
) -> List[Dict[str, Any]]:
    segments = model.transcribe(
        audio=os.path.join(output_dir, audio_file_path),
        verbose=verbose,
        **{
            'task': task,
            'language': language,
            'beam_size': beam_size,
        },
    ).segments

    return list(map(lambda segment: {
        'start': segment.start,
        'end': segment.end,
        'text': segment.text,
    }, segments))


def transcript_faster_whisper(
    audio_file_path: str,
    model: Union[whisper.Whisper, faster_whisper.WhisperModel],
    task: str,
    language: str,
    beam_size: int,
    output_dir: str,
    verbose: bool,
) -> List[Dict[str, Any]]:
    segments, info = model.transcribe(
        audio=os.path.join(output_dir, audio_file_path),
        task=task,
        language=language,
        beam_size=beam_size,
    )

    converted_segments = list()
    last_end = 0
    with tqdm(
        total=round(info.duration, 2),
        unit='sec',
        bar_format='{desc}: {percentage:.2f}%|{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]',
        disable=verbose is not False,
    ) as pbar:
        for segment in segments:
            converted_segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
            })

            pbar.update(
                segment.end - last_end
                if pbar.n + segment.end - last_end < info.duration
                else info.duration - pbar.n
            )

            last_end = segment.end

    return converted_segments
