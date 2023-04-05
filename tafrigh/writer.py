import os

from typing import Dict, List, Union

from tafrigh.config import Config
from tafrigh.types.transcript_type import TranscriptType


class Writer:
    def write_all(
        self,
        file_name: str,
        segments: List[Dict[str, Union[str, float]]],
        output_config: Config.Output,
    ) -> None:
        if output_config.save_files_before_compact:
            for output_format in output_config.output_formats:
                self.write(
                    output_format,
                    os.path.join(output_config.output_dir, f'{file_name}-original.{output_format}'),
                    segments,
                )

        if not output_config.save_files_before_compact or output_config.min_words_per_segment != 0:
            compacted_segments = self.compact_segments(segments, output_config.min_words_per_segment)

            for output_format in output_config.output_formats:
                self.write(
                    output_format,
                    os.path.join(output_config.output_dir, f'{file_name}.{output_format}'),
                    compacted_segments,
                )

    def write(
        self,
        format: TranscriptType,
        file_path: str,
        segments: List[Dict[str, Union[str, float]]],
    ) -> None:
        if format == TranscriptType.TXT:
            self.write_txt(file_path, segments)
        elif format == TranscriptType.SRT:
            self.write_srt(file_path, segments)
        elif format == TranscriptType.VTT:
            self.write_vtt(file_path, segments)

    def write_txt(
        self,
        file_path: str,
        segments: List[Dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_txt(segments))

    def write_srt(
        self,
        file_path: str,
        segments: List[Dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_srt(segments))

    def write_vtt(
        self,
        file_path: str,
        segments: List[Dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_vtt(segments))

    def generate_txt(self, segments: List[Dict[str, Union[str, float]]]) -> str:
        return '\n'.join(list(map(lambda segment: segment['text'].strip(), segments))) + '\n'

    def generate_srt(self, segments: List[Dict[str, Union[str, float]]]) -> str:
        return ''.join(
            f"{i}\n"
            f"{self._format_timestamp(segment['start'], include_hours=True, decimal_marker=',')} --> "
            f"{self._format_timestamp(segment['end'], include_hours=True, decimal_marker=',')}\n"
            f"{segment['text'].strip()}\n\n"
            for i, segment in enumerate(segments, start=1)
        )

    def generate_vtt(self, segments: List[Dict[str, Union[str, float]]]) -> str:
        return 'WEBVTT\n\n' + ''.join(
            f"{self._format_timestamp(segment['start'])} --> {self._format_timestamp(segment['end'])}\n"
            f"{segment['text'].strip()}\n\n"
            for segment in segments
        )

    def compact_segments(
        self,
        segments: List[Dict[str, Union[str, float]]],
        min_words_per_segment: int,
    ) -> List[Dict[str, Union[str, float]]]:
        if min_words_per_segment == 0:
            return segments

        compacted_segments = list()
        tmp_segment = None

        for segment in segments:
            if tmp_segment:
                tmp_segment['text'] += f" {segment['text'].strip()}"
                tmp_segment['end'] = segment['end']

                if len(tmp_segment['text'].split()) >= min_words_per_segment:
                    compacted_segments.append(tmp_segment)
                    tmp_segment = None
            elif len(segment['text'].split()) < min_words_per_segment:
                tmp_segment = dict(segment)
            elif len(segment['text'].split()) >= min_words_per_segment:
                compacted_segments.append(dict(segment))

        if tmp_segment:
            compacted_segments.append(tmp_segment)

        return compacted_segments

    def _write_to_file(self, file_path: str, content: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(content)

    def _format_timestamp(self, seconds: float, include_hours: bool = False, decimal_marker: str = '.') -> str:
        assert seconds >= 0, 'Non-negative timestamp expected'

        total_milliseconds = int(round(seconds * 1_000))

        hours, total_milliseconds = divmod(total_milliseconds, 3_600_000)
        minutes, total_milliseconds = divmod(total_milliseconds, 60_000)
        seconds, milliseconds = divmod(total_milliseconds, 1_000)

        if include_hours or hours > 0:
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
        else:
            time_str = f"{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"

        return time_str
