import csv
import json
import os

from pathlib import Path
from typing import Union

from tafrigh.config import Config
from tafrigh.types.transcript_type import TranscriptType
from tafrigh.utils import time_utils


class Writer:
    def write_all(
        self,
        file_name: str,
        segments: list[dict[str, Union[str, float]]],
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
        segments: list[dict[str, Union[str, float]]],
    ) -> None:
        if format == TranscriptType.TXT:
            self.write_txt(file_path, segments)
        elif format == TranscriptType.SRT:
            self.write_srt(file_path, segments)
        elif format == TranscriptType.VTT:
            self.write_vtt(file_path, segments)
        elif format == TranscriptType.CSV:
            self.write_csv(file_path, segments)
        elif format == TranscriptType.TSV:
            self.write_csv(file_path, segments, '\t')
        elif format == TranscriptType.JSON:
            self.write_json(file_path, segments)

    def write_txt(
        self,
        file_path: str,
        segments: list[dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_txt(segments))

    def write_srt(
        self,
        file_path: str,
        segments: list[dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_srt(segments))

    def write_vtt(
        self,
        file_path: str,
        segments: list[dict[str, Union[str, float]]],
    ) -> None:
        self._write_to_file(file_path, self.generate_vtt(segments))

    def write_csv(
        self,
        file_path: str,
        segments: list[dict[str, Union[str, float]]],
        delimiter=',',
    ) -> None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, fieldnames=['text', 'start', 'end'], delimiter=delimiter)
            writer.writeheader()
            writer.writerows(segments)

    def write_json(
        self,
        file_path: str,
        segments: list[dict[str, Union[str, float]]],
    ) -> None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(segments, fp, ensure_ascii=False, indent=2)

    def generate_txt(self, segments: list[dict[str, Union[str, float]]]) -> str:
        return '\n'.join(list(map(lambda segment: segment['text'].strip(), segments))) + '\n'

    def generate_srt(self, segments: list[dict[str, Union[str, float]]]) -> str:
        return ''.join(
            f"{i}\n"
            f"{time_utils.format_timestamp(segment['start'], include_hours=True, decimal_marker=',')} --> "
            f"{time_utils.format_timestamp(segment['end'], include_hours=True, decimal_marker=',')}\n"
            f"{segment['text'].strip()}\n\n"
            for i, segment in enumerate(segments, start=1)
        )

    def generate_vtt(self, segments: list[dict[str, Union[str, float]]]) -> str:
        return 'WEBVTT\n\n' + ''.join(
            f"{time_utils.format_timestamp(segment['start'])} --> {time_utils.format_timestamp(segment['end'])}\n"
            f"{segment['text'].strip()}\n\n"
            for segment in segments
        )

    def compact_segments(
        self,
        segments: list[dict[str, Union[str, float]]],
        min_words_per_segment: int,
    ) -> list[dict[str, Union[str, float]]]:
        if min_words_per_segment == 0:
            return segments

        compacted_segments = []
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

    def is_output_exist(self, file_name: str, output_config: Config.Output):
        if output_config.save_files_before_compact and not all(
            Path(output_config.output_dir, f'{file_name}-original.{output_format}').is_file()
            for output_format in output_config.output_formats
        ):
            return False

        if (not output_config.save_files_before_compact or output_config.min_words_per_segment != 0) and not all(
            Path(output_config.output_dir, f'{file_name}.{output_format}').is_file()
            for output_format in output_config.output_formats
        ):
            return False

        return True

    def _write_to_file(self, file_path: str, content: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(content)
