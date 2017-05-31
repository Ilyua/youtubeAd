import re
import sys

#!/usr/bin/python
import apiclient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(key_word):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=key_word,
    type="video",
    location='21.5922529,-158.1147114',
    locationRadius='10mi',
    part="id,snippet",
    maxResults=1
  ).execute()

  search_videos = []

  # Merge video ids
  for search_result in search_response.get("items", []):
    search_videos.append(search_result["id"]["videoId"])
  video_ids = ",".join(search_videos)

  # Call the videos.list method to retrieve location details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, recordingDetails'
  ).execute()

  videos = []

  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get("items", []):
    videos.append("{title}, ({lat},{lng}) https://www.youtube.com/watch?v={video_id}".format(
        title=video_result["snippet"]["title"],
        lat=video_result["recordingDetails"]["location"]["latitude"],
        lng=video_result["recordingDetails"]["location"]["longitude"],
        video_id=video_result["id"])
    )

  print("Videos:\n", "\n".join(videos), "\n")




def search_dictionary_parser(words_file_name):
    with open(words_file_name) as my_file:
        file_string = my_file.read()
    return re.findall(r'[а-я]+', file_string)    


youtube_search(sys.argv[0])
