from enum import Enum


class TranscriptType(Enum):
    ALL = 'all'
    TXT = 'txt'
    SRT = 'srt'
    VTT = 'vtt'
    NONE = 'none'

    def __str__(self):
        return self.value
