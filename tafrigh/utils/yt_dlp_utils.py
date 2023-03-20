import os

from typing import Any, Dict

import yt_dlp


def download_and_get_url_data(url: str, output_dir: str) -> Dict[str, Any]:
    return yt_dlp.YoutubeDL({
        'quiet': True,
        'verbose': False,
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
        ],
    }).extract_info(url, download=True)
