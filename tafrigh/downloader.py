import json
import os

from typing import Any

import yt_dlp


class Downloader:
  def __init__(self, yt_dlp_options: str, output_dir: str):
    self.yt_dlp_options = yt_dlp_options
    self.output_dir = output_dir

    self._initialize_youtube_dl_with_archive()
    self._initialize_youtube_dl_without_archive()

  def download(self, url: str, retries: int = 3, save_response: bool = False) -> dict[str, Any]:
    while True:
      self.youtube_dl_with_archive.download(url)
      url_data = self.youtube_dl_without_archive.extract_info(url, download=False)

      if retries <= 0 or not self._should_retry(url_data):
        break

      self._initialize_youtube_dl_with_archive()
      retries -= 1

    if save_response:
      self._save_response(url_data)

    return url_data

  def _initialize_youtube_dl_with_archive(self) -> None:
    self.youtube_dl_with_archive = yt_dlp.YoutubeDL(self._config(
      download_archive=os.path.join(self.output_dir, 'archive.txt'),
    ))

  def _initialize_youtube_dl_without_archive(self) -> None:
    self.youtube_dl_without_archive = yt_dlp.YoutubeDL(self._config(extract_flat=True))

  def _config(self, **kwargs: Any) -> dict[str, Any]:
    config = {
      'extract_audio': True,
      'format': 'bestaudio',
      'ignoreerrors': True,
      'outtmpl': os.path.join(self.output_dir, '%(id)s.%(ext)s'),
      'postprocessors': [
        {
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
        },
      ],
      'quiet': True,
      'verbose': False,
    }

    config.update(kwargs)
    config.update(json.loads(self.yt_dlp_options))

    return config

  def _should_retry(self, url_data: dict[str, Any]) -> bool:
    def file_exists(file_name: str) -> bool:
      extensions = ['mp3', 'wav', 'm4a', 'webm', 'opus']

      return any(os.path.exists(os.path.join(self.output_dir, f"{file_name}.{ext}")) for ext in extensions)

    if '_type' in url_data and url_data['_type'] == 'playlist':
      for entry in url_data['entries']:
        if entry and not file_exists(entry['id']):
          return True
    else:
      if not file_exists(url_data['id']):
        return True

    return False

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
