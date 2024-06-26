from pathlib import Path

from pydub import AudioSegment


def convert_to_mp3(file: Path) -> Path:
  audio_file = AudioSegment.from_file(str(file))
  converted_file_path = file.with_suffix('.mp3')
  audio_file.export(str(converted_file_path), format='mp3')
  return converted_file_path
