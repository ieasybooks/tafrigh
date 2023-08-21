import os
import tempfile

import numpy as np

from auditok.core import split
from scipy.io import wavfile


class AudioSplitter:
    def split(
        self,
        file_path: str,
        output_dir: str,
        min_dur: float = 0.5,
        max_dur: float = 15,
        max_silence: float = 0.5,
        energy_threshold: float = 50,
        expand_segments_with_noise: bool = False,
        noise_seconds: int = 1,
        noise_amplitude: int = 10,
    ) -> list[tuple[str, float, float]]:
        sampling_rate, data = self._read_audio(file_path)
        temp_file_name = self._write_temp_audio(sampling_rate, data)
        segments = self._split_audio(temp_file_name, min_dur, max_dur, max_silence, energy_threshold)

        os.remove(temp_file_name)

        if expand_segments_with_noise:
            expanded_segments = self._expand_segments_with_noise(
                segments,
                noise_seconds,
                noise_amplitude,
                sampling_rate,
                data.dtype,
            )
        else:
            expanded_segments = [(segment, segment.meta.start, segment.meta.end) for segment in segments]

        return self._save_segments(output_dir, sampling_rate, expanded_segments)

    def _read_audio(self, file_path: str) -> tuple[int, np.ndarray]:
        sampling_rate, data = wavfile.read(file_path)

        if len(data.shape) > 1 and data.shape[1] > 1:
            data = np.mean(data, axis=1)

        return sampling_rate, data

    def _write_audio(self, file_path: str, sampling_rate: int, data: np.ndarray) -> None:
        wavfile.write(file_path, sampling_rate, data.astype(np.int16))

    def _write_temp_audio(self, sampling_rate: int, data: np.ndarray) -> str:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file_name = temp_file.name
            self._write_audio(temp_file_name, sampling_rate, data)

        return temp_file_name

    def _split_audio(
        self,
        temp_file_name: str,
        min_dur: float,
        max_dur: float,
        max_silence: float,
        energy_threshold: float,
    ):
        return split(
            temp_file_name,
            min_dur=min_dur,
            max_dur=max_dur,
            max_silence=max_silence,
            energy_threshold=energy_threshold,
        )

    def _expand_segments_with_noise(
        self,
        segments: list,
        noise_seconds: int,
        noise_amplitude: int,
        sampling_rate: int,
        dtype: np.dtype,
    ) -> list[tuple[np.ndarray, float, float]]:
        expanded_segments = []

        for segment in segments:
            # Have different noise in the beginning and the end gave us better results :).
            prepend_noise = np.random.normal(0, noise_amplitude, int(noise_seconds * sampling_rate)).astype(dtype)
            append_noise = np.random.normal(0, noise_amplitude, int(noise_seconds * sampling_rate)).astype(dtype)

            expanded_segment = np.concatenate((prepend_noise, segment, append_noise))
            expanded_segments.append((expanded_segment, segment.meta.start, segment.meta.end))

        return expanded_segments

    def _save_segments(
        self,
        output_dir: str,
        sampling_rate: int,
        expanded_segments: list[tuple[np.ndarray, float, float]],
    ) -> list[tuple[str, float, float]]:
        segments = []

        for i, (expanded_segment, start, end) in enumerate(expanded_segments):
            output_file = os.path.join(output_dir, f"segment_{i + 1}.wav")
            self._write_audio(output_file, sampling_rate, expanded_segment)
            segments.append((output_file, start, end))

        return segments
