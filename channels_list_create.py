import re
import sys
import pprint
import list_create
import apiclient
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


import parser
from search_videos import youtube_search
import pprint

DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY
)



def uniquer(seq, f=None):
    """ Keeps earliest occurring item of each f-defined equivalence class """
    if f is None:    # f's default is the identity function f(x) -> x
        def f(x): return x
    already_seen = set( )
    result = [  ]
    for item in seq:
        marker = f(item)
        if marker not in already_seen:
             already_seen.add(marker)
             result.append(item)
    return result


def create_channels_list(videos_array):
    channels_ids = []
    channels_array = []
    #pprint.pprint(videos_array)
    for video in videos_array:
        channels_ids.append(video['snippet']['channelId'])
    pprint.pprint(channels_ids)
    print('+++++')
    channels_ids = uniquer(channels_ids)#dict([(item, None) for item in channels_ids]).keys()
    pprint.pprint(channels_ids)
    for channel_id in channels_ids:
        result = youtube.channels().list(
            # part="snippet,auditDetails,contentDetails" +
            # ",contentOwnerDetails,statistics,localizations,status",
            part = "snippet,contentOwnerDetails,statistics,localizations,status",
            id=channel_id
        ).execute()
        channels_array.extend(result.get("items", []))
    #pprint.pprint(channels_array)
    pprint.pprint(len(channels_array))
    return channels_array


PAGES_NUMBER = 3
word_list = parser.search_dictionary_parser('5000lemma.txt')
pprint.pprint('--------')
# for word in word_list:
word = word_list[0]
dict_videos = []
dict_videos = youtube_search(word, PAGES_NUMBER)
print(1)
create_channels_list(dict_videos)
