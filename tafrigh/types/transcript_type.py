from enum import Enum


class TranscriptType(Enum):
    NONE = 'none'
    VTT = 'vtt'
    SRT = 'srt'
    TXT = 'txt'

    def __str__(self):
        return self.value
