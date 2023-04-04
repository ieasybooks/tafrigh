import json
import os

from typing import Any, Dict, List

import yt_dlp


class Downloader:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.youtube_dl = yt_dlp.YoutubeDL(self._config())

    def _config(self) -> Dict[str, Any]:
        return {
            'quiet': True,
            'verbose': False,
            'format': 'wav/bestaudio/best',
            'outtmpl': os.path.join(self.output_dir, '%(id)s.%(ext)s'),
            'ignoreerrors': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                },
            ],
        }

    def download(self, url: str, save_response: bool = False) -> Dict[str, Any]:
        url_data = self.youtube_dl.extract_info(url, download=True)

        if save_response:
            self._save_response(url)

        return url_data

    def _save_response(self, url: str) -> None:
        url_data = self.youtube_dl.extract_info(url)

        if '_type' in url_data and url_data['_type'] == 'playlist':
            for entry in url_data['entries']:
                if entry:
                    self._remove_postprocessors(entry['requested_downloads'])
        else:
            self._remove_postprocessors(url_data['requested_downloads'])

        file_path = os.path.join(self.output_dir, f"{url_data['id']}.json")

        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(url_data, fp, indent=2, ensure_ascii=False)

    def _remove_postprocessors(self, requested_downloads: List[Dict[str, Any]]) -> None:
        for requested_download in requested_downloads:
            requested_download.pop('__postprocessors')
