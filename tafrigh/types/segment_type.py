from typing import NotRequired, TypedDict


class SegmentType(TypedDict):
  text: str
  start: float
  end: float
  url: NotRequired[str]
  file_path: NotRequired[str]
