import io
import os
import subprocess

from concurrent.futures import ThreadPoolExecutor

from auditok import AudioRegion
from auditok.core import split
from pydub import AudioSegment
from pydub.generators import WhiteNoise
from pydub.utils import mediainfo


LARGE_FILE_DURATION = 3 * 60 * 60
MAX_FILE_DURATION = 1 * 60 * 60


class AudioSplitter:
  def split(
    self,
    file_path: str,
    min_dur: float = 0.5,
    max_dur: float = 15,
    max_silence: float = 0.5,
    energy_threshold: float = 50,
    noise_seconds: int = 1,
    noise_amplitude: int = 0,
    from_split_large_file: bool = False,
  ) -> list[tuple[bytes, float, float]]:
    file_info = mediainfo(file_path)

    if (
      not from_split_large_file
      and ('duration' not in file_info or float(file_info['duration']) > LARGE_FILE_DURATION)
    ):
      return self._split_large_file(
        file_path,
        min_dur,
        max_dur,
        max_silence,
        energy_threshold,
        noise_seconds,
        noise_amplitude,
      )
    else:
      return self._segments_to_data([
        (
          self._expand_segment_with_noise(segment, noise_seconds, noise_amplitude),
          segment.meta.start,
          segment.meta.end,
        ) for segment in split(
          file_path,
          min_dur=min_dur,
          max_dur=max_dur,
          max_silence=max_silence,
          energy_threshold=energy_threshold,
          audio_format='mp3',
        )
      ])

  def _split_large_file(
    self,
    file_path: str,
    min_dur: float,
    max_dur: float,
    max_silence: float,
    energy_threshold: float,
    noise_seconds: int,
    noise_amplitude: int,
  ) -> list[tuple[bytes, float, float]]:
    duration = float(mediainfo(file_path)['duration'])

    segments = []

    base_name, ext = os.path.splitext(file_path)
    output_file = f"{base_name}_part{ext}"

    for i in range(0, int(duration), MAX_FILE_DURATION):
      start_time = i
      end_time = min(i + MAX_FILE_DURATION, duration)

      with open(os.devnull, 'w') as devnull:
        subprocess.run(
          ['ffmpeg', '-y', '-i', file_path, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', output_file],
          stdout=devnull,
          stderr=devnull,
        )

      part_segments = self.split(
        output_file,
        min_dur,
        max_dur,
        max_silence,
        energy_threshold,
        noise_seconds,
        noise_amplitude,
        True,
      )

      segments.extend([(segment[0], segment[1] + start_time, segment[2] + start_time) for segment in part_segments])

      os.remove(output_file)

    return segments

  def _expand_segment_with_noise(self, segment: AudioRegion, noise_seconds: int, noise_amplitude: int) -> AudioSegment:
    audio_segment = AudioSegment(
      segment.data,
      frame_rate=segment.sampling_rate,
      sample_width=segment.sample_width,
      channels=segment.channels,
    )

    pre_noise = WhiteNoise().to_audio_segment(duration=noise_seconds * 1000, volume=noise_amplitude)
    post_noise = WhiteNoise().to_audio_segment(duration=noise_seconds * 1000, volume=noise_amplitude)

    return pre_noise + audio_segment + post_noise

  def _segments_to_data(self, segments: list[tuple[AudioSegment, float, float]]) -> list[tuple[bytes, float, float]]:
    def process_segment(segment: tuple[AudioSegment, float, float]) -> tuple[bytes, float, float]:
      output_buffer = io.BytesIO()
      segment[0].export(output_buffer, format='mp3')

      return (output_buffer.getvalue(), segment[1], segment[2])

    with ThreadPoolExecutor() as executor:
      segments_data = list(executor.map(process_segment, segments))

    return segments_data
