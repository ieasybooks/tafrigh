import sys


if sys.version_info < (3, 11):
  from typing_extensions import NotRequired, TypedDict
else:
  from typing import NotRequired, TypedDict


class SegmentType(TypedDict):
  text: str
  start: float
  end: float
  url: NotRequired[str]
  file_path: NotRequired[str]
