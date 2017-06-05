import re
import sys
from pprint import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


class Downloader(object):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    def __init__(self, number_of_page):
        self.number_of_page = number_of_page
        self.videos_info = []
        self.channels_array = []
        self.channels_of_comments_array = []
 
    @staticmethod
    def parse_feq_dictionary(words_file_name):
        REGEX = re.compile('(?P<num>\d+) (?P<freq>[\d\.]+) (?P<phrase>[^ ]+) (?P<type>[a-zA-Z]+)')

        with open(words_file_name, 'r') as my_file:
            for nline, line in enumerate(my_file.readlines()):
                match = REGEX.match(line) 

                if match is None: 
                    raise Exception('Problem with format in file {} (line {})'.format(words_file_name, nline))  
                
                yield match.group('phrase') 


    def search_by_all_key(self):
        words_list = self.search_dictionary_parser('5000lemma.txt')
        for word in words_list:
            self.youtube_search(word)

    def search_by_all_key_for_one_word(self, number):
        words_list = self.search_dictionary_parser('5000lemma.txt')
        word = words_list[number]
        self.youtube_search(word)

    def create_channels_list(self, videos_array):
        channels_ids = []
        for video in videos_array:
            channels_ids.append(video['snippet']['channelId'])
        channels_ids = self.uniquer(channels_ids)
        for channel_id in channels_ids:
            result = self.youtube.channels().list(
                part="snippet,contentOwnerDetails,statistics,localizations,status",
                id=channel_id
            ).execute()
            self.channels_array.extend(result.get("items", []))
        return self.channels_array

    def create_channels_of_comments_list(self, videos_array):
        channels_ids = []
        video_comment_threads = []
        for video in videos_array:
            video_id = video['id']
            results = self.youtube.commentThreads().list(
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
        channels_ids = self.uniquer(channels_ids)
        for channel_id in channels_ids:
            result = self.youtube.channels().list(
                part="snippet,contentOwnerDetails,statistics,localizations,status",
                id=channel_id
            ).execute()
            self.channels_of_comments_array.extend(result.get("items", []))
        return self.channels_of_comments_array

#####################################################################

    def youtube_search(self, key_word):
        page_token = None
        search_videos = []
        pprint(key_word)
        for number in range(self.number_of_page):
            search_response = self.youtube.search().list(
                q=key_word,
                type="video",
                part="id,snippet",
                maxResults=10,
                pageToken=page_token
            ).execute()
            page_token = search_response.get("nextPageToken", None)
            if page_token == None:
                break
            for search_result in search_response.get("items", []):
                search_videos.append(search_result["id"]["videoId"])
        videos_info = []
        for video_id in search_videos:
            video_response = self.youtube.videos().list(
                id=video_id,
                part='snippet, recordingDetails'
            ).execute()
            self.videos_info.extend(video_response.get("items", []))
        return self.videos_info

    def uniquer(self, seq, f=None):
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
