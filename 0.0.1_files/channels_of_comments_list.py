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
    already_seen = set()
    result = []
    for item in seq:
        marker = f(item)
        if marker not in already_seen:
            already_seen.add(marker)
            result.append(item)
    return result

####################################################
# def get_comment_threads(youtube, video_id):
#   results = youtube.commentThreads().list(
#     part="snippet",
#     videoId=video_id,
#     textFormat="plainText"
#   ).execute()

#   for item in results["items"]:
#     comment = item["snippet"]["topLevelComment"]
#     author = comment["snippet"]["authorDisplayName"]
#     text = comment["snippet"]["textDisplay"]
#     print "Comment by %s: %s" % (author, text)

#   return results["items"]


# # Call the API's comments.list method to list the existing comment replies.
# def get_comments(youtube, parent_id):
#   results = youtube.comments().list(
#     part="snippet",
#     parentId=parent_id,
#     textFormat="plainText"
#   ).execute()

#   for item in results["items"]:
#     author = item["snippet"]["authorDisplayName"]
#     text = item["snippet"]["textDisplay"]
#     print "Comment by %s: %s" % (author, text)

#   return results["items"]

#   video_comment_threads = get_comment_threads(youtube, args.videoid)
#     parent_id = video_comment_threads[0]["id"]
#     insert_comment(youtube, parent_id, args.text)
#     video_comments = get_comments(youtube, parent_id)
####################################################
def create_channels_of_comments_list(videos_array):
    channels_ids = []
    channels_array = []
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
        #pprint.pprint(results)
        #parent_id = video_comment_threads[0]["id"]
        # print(parent_id)
        # comments = youtube.comments().list(
        #     part="snippet",
        #     parentId=parent_id,
        #     textFormat="plainText"
        # ).execute()
        # video_comments = comments["items"]
        # pprint.pprint(video_comments)
        for comment in video_comment_threads:
            channels_ids.append(comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])

    # pprint.pprint(videos_array)

    pprint.pprint(channels_ids)
    print('+++++')
    # dict([(item, None) for item in channels_ids]).keys()
    channels_ids = uniquer(channels_ids)
    pprint.pprint(channels_ids)
    for channel_id in channels_ids:
        result = youtube.channels().list(
            # part="snippet,auditDetails,contentDetails" +
            # ",contentOwnerDetails,statistics,localizations,status",
            part="snippet,contentOwnerDetails,statistics,localizations,status",
            id=channel_id
        ).execute()
        channels_array.extend(result.get("items", []))
    pprint.pprint(channels_array)
    pprint.pprint(len(channels_array))
    return channels_array


PAGES_NUMBER = 1
word_list = parser.search_dictionary_parser('5000lemma.txt')
pprint.pprint('--------')
# for word in word_list:
word = word_list[0]
dict_videos = []
dict_videos = youtube_search(word, PAGES_NUMBER)
print(1)
create_channels_of_comments_list(dict_videos)
