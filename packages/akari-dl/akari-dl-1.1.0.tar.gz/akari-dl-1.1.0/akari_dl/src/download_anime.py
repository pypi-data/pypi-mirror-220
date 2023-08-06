"""
  Download an anime based on user-configuration given desired anime is found on desired website.
"""

import os
import requests.exceptions

from akari_dl.src.log_response import log_response

def download_episodes(self, folder_path=os.PathLike, episodes=list):
  """
    Download all (unless specified otherwise) episodes of an anime
    into a folder of the anime's name inside the user-provided output path.
  """
  ep_count = 0

  for episode in episodes:
    ep_count += 1

    try:
      if self.name == "chauthanh":
        self.response = self.session.get(f"{self.url}/anime/{episode.attrs['href'][3:]}", timeout=30)
      else:
        self.response = self.session.get(f"{self.url}{episode.attrs['href']}", timeout=30)
      anchor = self.response.html.find(self.anchors[2], first=True)
      self.endpoint = anchor.attrs["href"]
    except AttributeError:
      print("Video file not found - skipping episode.")
      continue

    file_format = self.endpoint[-3:]

    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    try:
      if self.name == "chauthanh":
        self.response = self.session.get(f"{self.url}/anime/download/{self.endpoint[3:]}", timeout=30)
      else:
        self.response = self.session.get(self.endpoint, timeout=30)
    except requests.exceptions.MissingSchema:
      print("Video file not found - skipping episode.")
      continue

    print(f"Downloading episode {ep_count} from {self.endpoint}")
    file_path = os.path.join(folder_path, f"Episode {ep_count}.{file_format}")
    with open(file_path, "wb") as video_file:
      for chunk in self.response.iter_content(1024):
        video_file.write(chunk)
    print(f"Episode {ep_count} downloaded to {file_path}")


def download_anime(self):
  """
    Download user specified anime by scraping links until reaching a video file source.
  """
  self.response = self.session.get(f"{self.url}{self.endpoint}")
  episodes = self.response.html.find(self.anchors[1]) # Episodes anchors

  episodes_regular, episodes_special = [], []
  episodes.reverse()

  if self.name == "tokyoinsider":
    for episode in episodes:
      match episode.find("em", first=True).text:
        case "episode":
          episodes_regular.append(episode)
        case _:
          episodes_special.append(episode)
  else:
    episodes_regular = episodes

  anime_slug = self.anime
  for char in "/><\"\:|?*":
    anime_slug = anime_slug.replace(char, "")

  folder_path = os.path.join(self.output_path, anime_slug)

  download_episodes(self, folder_path, episodes_regular)

  if self.specials_enabled is True:
    folder_path = os.path.join(self.output_path, anime_slug, "Specials")

    download_episodes(self, folder_path, episodes_special)
    # try:
      # download_episodes(self, folder_path, episodes_special)
    # except Exception as error:
      # print(f"Download failed: {error}")
      # exit()

  return f"Finished downloading {self.anime}."
