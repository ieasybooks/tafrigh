from enum import Enum


class TranscriptType(Enum):
    ALL = 'all'
    TXT = 'txt'
    SRT = 'srt'
    VTT = 'vtt'
    CSV = 'csv'
    TSV = 'tsv'
    JSON = 'json'
    NONE = 'none'

    def __str__(self):
        return self.value
