import json
import os

from typing import Any

import yt_dlp


class Downloader:
  def __init__(self, output_dir: str):
    self.output_dir = output_dir

    self._initialize_youtube_dl()

  def download(self, url: str, save_response: bool = False) -> dict[str, Any]:
    url_data: dict[str, Any] = {}

    while True:
      old_mp3_count = self._mp3_count()
      current_url_data = self.youtube_dl.extract_info(url)

      if old_mp3_count == self._mp3_count():
        break
      else:
        if url_data == {}:
          url_data = current_url_data
        else:
          url_data = self._merge_yt_dlp_responses(url_data, current_url_data)

      self._initialize_youtube_dl()

    if save_response:
      self._save_response(url_data)

    return url_data

  def _initialize_youtube_dl(self) -> None:
    self.youtube_dl = yt_dlp.YoutubeDL(self._config(download_archive=os.path.join(self.output_dir, 'archive.txt')))

  def _config(self, **kwargs: Any) -> dict[str, Any]:
    config = {
      'quiet': True,
      'verbose': False,
      'format': 'bestaudio',
      'extract_audio': True,
      'outtmpl': os.path.join(self.output_dir, '%(id)s.%(ext)s'),
      'ignoreerrors': True,
      'postprocessors': [
        {
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
        },
      ],
    }

    config.update(kwargs)

    return config

  def _mp3_count(self) -> int:
    return len([file_name for file_name in os.listdir(self.output_dir) if file_name.endswith('.mp3')])

  def _save_response(self, url_data: dict[str, Any]) -> None:
    file_path = os.path.join(self.output_dir, f"{url_data['id']}.json")

    if os.path.exists(file_path):
      old_url_data = json.load(open(file_path, encoding='utf-8'))

      url_data = self._merge_yt_dlp_responses(old_url_data, url_data)

    with open(file_path, 'w', encoding='utf-8') as fp:
      json.dump(self.youtube_dl.sanitize_info(url_data), fp, indent=2, ensure_ascii=False)

  def _merge_yt_dlp_responses(self, old_response: dict[str, Any], new_response: dict[str, Any]) -> dict[str, Any]:
    if 'entries' not in old_response.keys() or 'entries' not in new_response.keys():
      raise ValueError('No entries found in the responses')

    seen_ids = set()
    unique_entries = []

    for entry in old_response['entries'] + new_response['entries']:
      if entry['id'] not in seen_ids:
        seen_ids.add(entry['id'])
        unique_entries.append(entry)

    new_response['entries'] = unique_entries

    return new_response
