import re
import sys
import pprint
import apiclient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


class Downloader:

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    def __init__(number_of page):
        self.number_of_page = number_of_page
        self.videos_info = []
        self.channels_array = []
        self.channels__of_comments_array = []

    def youtube_search(key_word):
        page_token = None
        search_videos = []
        for number in range(self.number_of_pages):
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
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet, recordingDetails'
            ).execute()
        videos_info.extend(video_response.get("items", []))
        return videos_info

    def create_channels_list(videos_array):
        channels_ids = []
        for video in videos_array:
            channels_ids.append(video['snippet']['channelId'])
        channels_ids = uniquer(channels_ids)
        for channel_id in channels_ids:
            result = youtube.channels().list(
                part="snippet,contentOwnerDetails,statistics,localizations,status",
                id=channel_id
            ).execute()
            channels_array.extend(result.get("items", []))
        return channels_array

    def create_channels_of_comments_list(videos_array):
        channels_ids = []
        video_comment_threads = []
        for video in videos_array:
            video_id = video['id']
            pprint.pprint(video_id)
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText"
            ).execute()
            video_comment_threads = results["items"]
            for comment in video_comment_threads:
                channels_ids.append(comment
                                    ['snippet']
                                    ['topLevelComment']
                                    ['snippet']
                                    ['authorChannelId']
                                    ['value'])
        channels_ids = uniquer(channels_ids)
        for channel_id in channels_ids:
            result = youtube.channels().list(
                part="snippet,contentOwnerDetails,statistics,localizations,status",
                id=channel_id
            ).execute()
            channels__of_comments_array.extend(result.get("items", []))
        return channels__of_comments_array

    private:

    def search_dictionary_parser(words_file_name):
    with open(words_file_name) as my_file:
        file_string = my_file.read()
    return re.findall(r'[а-я]+', file_string)

    def uniquer(seq, f=None):
    """ Keeps earliest occurring item of each f-defined equivalence class """
    if f is None:    # f's default is the identity function f(x) -> x
        def f(x): return x
    already_seen = set()
    result = []
    for item in seq:
        marker = f(item)
        if marker not in already_seen:
            already_seen.add(marker)
            result.append(item)
    return result
