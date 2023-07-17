import warnings

from typing import Dict, List, Union

import faster_whisper
import whisper
import whisper_jax

from tqdm import tqdm

from tafrigh.config import Config
from tafrigh.types.whisper.type_hints import WhisperModel


class WhisperRecognizer:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def recognize(
        self,
        file_path: str,
        model: WhisperModel,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            if isinstance(model, whisper.Whisper):
                return self._recognize_stable_whisper(file_path, model, whisper_config)
            elif isinstance(model, faster_whisper.WhisperModel):
                return self._recognize_faster_whisper(file_path, model, whisper_config)
            elif isinstance(model, whisper_jax.FlaxWhisperPipline):
                return self._recognize_jax_whisper(file_path, model, whisper_config)

    def _recognize_stable_whisper(
        self,
        audio_file_path: str,
        model: whisper.Whisper,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments = model.transcribe(
            audio=audio_file_path,
            verbose=self.verbose,
            task=whisper_config.task,
            language=whisper_config.language,
            beam_size=whisper_config.beam_size,
        ).segments

        return [
            {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
            }
            for segment in segments
        ]

    def _recognize_faster_whisper(
        self,
        audio_file_path: str,
        model: faster_whisper.WhisperModel,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments, info = model.transcribe(
            audio=audio_file_path,
            task=whisper_config.task,
            language=whisper_config.language,
            beam_size=whisper_config.beam_size,
        )

        converted_segments = []
        last_end = 0
        with tqdm(
            total=round(info.duration, 2),
            unit='sec',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]',
            disable=self.verbose is not False,
        ) as pbar:
            for segment in segments:
                converted_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                })

                pbar_update = min(segment.end - last_end, info.duration - pbar.n)
                pbar.update(pbar_update)
                last_end = segment.end

        return converted_segments

    def _recognize_jax_whisper(
        self,
        audio_file_path: str,
        model: whisper_jax.FlaxWhisperPipline,
        whisper_config: Config.Whisper,
    ) -> List[Dict[str, Union[str, float]]]:
        segments = model(
            audio_file_path,
            task=whisper_config.task,
            language=whisper_config.language,
            return_timestamps=True,
        )['chunks']

        return [
            {
                'start': segment['timestamp'][0],
                'end': segment['timestamp'][1],
                'text': segment['text'].strip(),
            }
            for segment in segments
        ]
