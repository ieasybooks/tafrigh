from typing import Iterator, TextIO


def write_vtt(transcript: Iterator[dict], file: TextIO):
    file.write('WEBVTT\n\n')

    for segment in transcript:
        file.write(f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n")
        file.write(f"{segment['text'].strip().replace('-->', '->')}\n\n")


def write_srt(transcript: Iterator[dict], file: TextIO):
    for i, segment in enumerate(transcript, start=1):
        start_time = format_timestamp(segment['start'], include_hours=True, decimal_marker=',')
        end_time = format_timestamp(segment['end'], include_hours=True, decimal_marker=',')

        file.write(f"{i}\n")
        file.write(f"{start_time} --> {end_time}\n")
        file.write(f"{segment['text'].strip().replace('-->', '->')}\n\n")


def format_timestamp(seconds: float, include_hours: bool = False, decimal_marker: str = '.'):
    assert seconds >= 0, 'non-negative timestamp expected'

    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
