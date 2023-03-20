from enum import Enum


class TranscriptType(Enum):
    SRT = 'srt'
    VTT = 'vtt'

    def __str__(self):
        return self.value
