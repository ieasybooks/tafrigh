import warnings

from typing import Generator, Union

import faster_whisper
import whisper

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
    ) -> Generator[dict[str, float], None, list[dict[str, Union[str, float]]]]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            if isinstance(model, whisper.Whisper):
                whisper_generator = self._recognize_stable_whisper(file_path, model, whisper_config)
            elif isinstance(model, faster_whisper.WhisperModel):
                whisper_generator = self._recognize_faster_whisper(file_path, model, whisper_config)

            while True:
                try:
                    yield next(whisper_generator)
                except StopIteration as e:
                    return e.value

    def _recognize_stable_whisper(
        self,
        audio_file_path: str,
        model: whisper.Whisper,
        whisper_config: Config.Whisper,
    ) -> Generator[dict[str, float], None, list[dict[str, Union[str, float]]]]:
        yield {'progress': 0.0, 'remaining_time': None}

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
    ) -> Generator[dict[str, float], None, list[dict[str, Union[str, float]]]]:
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
                converted_segments.append(
                    {
                        'start': segment.start,
                        'end': segment.end,
                        'text': segment.text.strip(),
                    }
                )

                pbar_update = min(segment.end - last_end, info.duration - pbar.n)
                pbar.update(pbar_update)
                last_end = segment.end

                yield {
                    'progress': round(pbar.n / pbar.total * 100, 2),
                    'remaining_time': (pbar.total - pbar.n) / pbar.format_dict['rate']
                    if pbar.format_dict['rate'] and pbar.total
                    else None,
                }

        return converted_segments
