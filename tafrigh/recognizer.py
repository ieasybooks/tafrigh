import warnings

from typing import Any, Dict, List, Union

import faster_whisper
import whisper

from tqdm import tqdm


class Recognizer:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def recognize_whisper(
        self,
        file_path: str,
        model: Union[whisper.Whisper, faster_whisper.WhisperModel],
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Any]]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            if isinstance(model, whisper.Whisper):
                return self._recognize_stable_whisper(
                    file_path,
                    model,
                    task,
                    language,
                    beam_size,
                )
            elif isinstance(model, faster_whisper.WhisperModel):
                return self._recognize_faster_whisper(
                    file_path,
                    model,
                    task,
                    language,
                    beam_size,
                )

    def _recognize_stable_whisper(
        self,
        audio_file_path: str,
        model: whisper.Whisper,
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Any]]:
        segments = model.transcribe(
            audio=audio_file_path,
            verbose=self.verbose,
            task=task,
            language=language,
            beam_size=beam_size,
        ).segments

        return [
            {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
            }
            for segment in segments
        ]

    def _recognize_faster_whisper(
        self,
        audio_file_path: str,
        model: faster_whisper.WhisperModel,
        task: str,
        language: str,
        beam_size: int,
    ) -> List[Dict[str, Any]]:
        segments, info = model.transcribe(
            audio=audio_file_path,
            task=task,
            language=language,
            beam_size=beam_size,
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
                    'text': segment.text,
                })

                pbar_update = min(segment.end - last_end, info.duration - pbar.n)
                pbar.update(pbar_update)
                last_end = segment.end

        return converted_segments
