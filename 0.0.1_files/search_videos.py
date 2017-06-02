import re
import sys
import pprint

import apiclient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(key_word, pages_number):
    page_token = None

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_videos = []

    for number in range(pages_number):


        search_response = youtube.search().list(
            q=key_word,
            type="video",
            part="id,snippet",
            maxResults=1,
            pageToken=page_token
        ).execute()

        page_token = search_response.get("nextPageToken", None)
        if page_token == None:
            break

        for search_result in search_response.get("items", []):
            search_videos.append(search_result["id"]["videoId"])
    videos_info = []
    for video_id in search_videos:

      # Call the videos.list method to retrieve location details for each
      # video.
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet, recordingDetails'
        ).execute()
        pprint.pprint(video_id)

        videos_info.extend(video_response.get("items", []))


    return videos_info
