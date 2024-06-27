import io

from concurrent.futures import ThreadPoolExecutor

from auditok import AudioRegion
from auditok.core import split
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from pydub.generators import WhiteNoise
from pydub.utils import mediainfo


MAX_FILE_DURATION = 4 * 60 * 60


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
  ) -> list[tuple[bytes, float, float]]:
    try:
      segments = [
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
          large_file=float(mediainfo(file_path)['duration']) > MAX_FILE_DURATION,
        )
      ]
    except CouldntDecodeError:
      segments = [
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
          large_file=True,
        )
      ]

    return self._segments_to_data(segments)

  def _expand_segment_with_noise(self, segment: AudioRegion, noise_seconds: int, noise_amplitude: int) -> AudioSegment:
    audio_segment = AudioSegment(
      segment._data,
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
