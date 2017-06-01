import re
import sys


import apiclient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(key_word,page_token = None):
    youtube = build(
      YOUTUBE_API_SERVICE_NAME,
      YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY
      )

    search_response = youtube.search(page_token).list(
        q=key_word,
        type="video",
        part="id,snippet",
        maxResults=10
    ).execute()
    print(search_response)
    search_videos = []

    for search_result in search_response.get("items", []):
        search_videos.append(search_result["id"]["videoId"])
    video_ids = ",".join(search_videos)

    video_response = youtube.videos().list(
      id=video_ids,
      part='snippet,recordingDetails'
    ).execute()

    videos = []
    return video_response.get("items", [])
