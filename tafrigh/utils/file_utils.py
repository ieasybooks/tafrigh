import mimetypes

from pathlib import Path


mimetypes.init()


def filter_media_files(paths: list[Path]) -> list[Path]:
    # Filter out non audio or video files
    filtered_media_files: list[str] = []
    for path in paths:
        mime = mimetypes.guess_type(path)[0]
        if mime is None:
            continue
        mime_type = mime.split('/')[0]
        if mime_type not in ('audio', 'video'):
            continue
        filtered_media_files.append(path)
    return filtered_media_files
