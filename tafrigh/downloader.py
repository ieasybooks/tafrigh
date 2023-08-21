import json
import os

from typing import Any, Union

import yt_dlp


class Downloader:
    def __init__(self, playlist_items: str, output_dir: str):
        self.playlist_items = playlist_items
        self.output_dir = output_dir
        self.youtube_dl_with_archive = yt_dlp.YoutubeDL(self._config(os.path.join(self.output_dir, 'archive.txt')))
        self.youtube_dl_without_archive = yt_dlp.YoutubeDL(self._config(False))

    def _config(self, download_archive: Union[str, bool]) -> dict[str, Any]:
        return {
            'quiet': True,
            'verbose': False,
            'format': 'wav/bestaudio/best',
            'outtmpl': os.path.join(self.output_dir, '%(id)s.%(ext)s'),
            'ignoreerrors': True,
            'download_archive': download_archive,
            'playlist_items': self.playlist_items,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                },
            ],
        }

    def download(self, url: str, save_response: bool = False) -> dict[str, Any]:
        self.youtube_dl_with_archive.download(url)
        url_data = self.youtube_dl_without_archive.extract_info(url, download=False)

        if save_response:
            self._save_response(url_data)

        return url_data

    def _save_response(self, url_data: dict[str, Any]) -> None:
        if '_type' in url_data and url_data['_type'] == 'playlist':
            for entry in url_data['entries']:
                if entry and 'requested_downloads' in entry:
                    self._remove_postprocessors(entry['requested_downloads'])
        elif 'requested_downloads' in url_data:
            self._remove_postprocessors(url_data['requested_downloads'])

        file_path = os.path.join(self.output_dir, f"{url_data['id']}.json")

        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(url_data, fp, indent=2, ensure_ascii=False)

    def _remove_postprocessors(self, requested_downloads: list[dict[str, Any]]) -> None:
        for requested_download in requested_downloads:
            requested_download.pop('__postprocessors')
