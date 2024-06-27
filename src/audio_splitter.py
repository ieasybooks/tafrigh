import io

from auditok import AudioRegion
from auditok.core import split
from pydub import AudioSegment
from pydub.generators import WhiteNoise


class AudioSplitter:
  def split(
    self,
    file_path: str,
    min_dur: float = 0.5,
    max_dur: float = 15,
    max_silence: float = 0.5,
    energy_threshold: float = 50,
    expand_segments_with_noise: bool = False,
    noise_seconds: int = 1,
    noise_amplitude: int = 0,
  ) -> list[tuple[str, float, float]]:
    segments = split(
      file_path,
      min_dur=min_dur,
      max_dur=max_dur,
      max_silence=max_silence,
      energy_threshold=energy_threshold,
    )

    if expand_segments_with_noise:
      segments = [
        (
          self._expand_segment_with_noise(segment, noise_seconds, noise_amplitude),
          segment.meta.start,
          segment.meta.end,
        ) for segment in segments
      ]

    return self._semgnets_to_data(segments)

  def _expand_segment_with_noise(
    self,
    segment: AudioRegion,
    noise_seconds: int,
    noise_amplitude: int,
  ) -> AudioSegment:

    audio_segment = AudioSegment(
      segment._data,
      frame_rate=segment.sampling_rate,
      sample_width=segment.sample_width,
      channels=segment.channels,
    )

    pre_noise = WhiteNoise().to_audio_segment(duration=noise_seconds * 1000, volume=noise_amplitude)
    post_noise = WhiteNoise().to_audio_segment(duration=noise_seconds * 1000, volume=noise_amplitude)

    return pre_noise + audio_segment + post_noise

  def _semgnets_to_data(
    self,
    segments: list[AudioSegment | tuple[AudioSegment, float, float]],
  ) -> list[tuple[bytes, float, float]]:
    segment_data = []

    for segment in segments:
      output_buffer = io.BytesIO()

      if isinstance(segment, tuple):
        segment[0].export(output_buffer, format='mp3')
        segment_data.append((output_buffer.getvalue(), segment[1], segment[2]))
      else:
        segment.export(output_buffer, format='mp3')
        segment_data.append((output_buffer.getvalue(), segment.meta.start, segment.meta.end))

    return segment_data
