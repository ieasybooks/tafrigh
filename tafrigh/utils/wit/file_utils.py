from pathlib import Path

from pydub import AudioSegment


def convert_to_wav(file: Path) -> Path:
    audio_file = AudioSegment.from_file(str(file))
    converted_file_path = file.with_suffix('.wav')
    audio_file.export(str(converted_file_path), format='wav')
    return converted_file_path
