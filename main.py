from pprint import pprint
from youtube_apiclient import ApiClient
from key_phrase_parser import parse_feq_dictionary
from pymongo import MongoClient
import sys
client = MongoClient()
db = client.my_db
channels_coll = db.channels
videos_coll = db.videos
comments_coll = db.comments

#db.dropDatabase()
phrases_list = (list(parse_feq_dictionary('5000lemma.txt')))[int(sys.argv[2])]
client = ApiClient(sys.argv[1])

channel_ids = set()

for i, phrase in enumerate(phrases_list):
    if i >= 20:
        break
videos_ids = client.search_videos_by_key_phrase(phrase)
for video_id in videos_ids:
    channel_ids.update({comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value'] for comment in client.get_videos_main_comments(video_id)})
    for comment in client.get_videos_main_comments(video_id):
        comments_coll.insert(comment)
    videos_coll.insert(client.get_video_info(video_id))
for channel_id in channel_ids:
    channels_coll.insert(client.get_channel_info(channel_id))




















































# downloader = Downloader(number_of_page=1)

# downloader.download_videos('5000lemma.txt', limit=1)


# downloader.create_channels_list({video['snippet']['channelId'] for video in downloader.videos_info})
# comments_threads=downloader.get_videos_comments_threads({video['snippet']['channelId'] for video in downloader.videos_info})
# downloader.get_videos_comments_owners({comment
#                                     ['snippet']
#                                     ['topLevelComment']
#                                     ['snippet']
#                                     ['authorChannelId']
#                                     ['value'] for comment in comments_threads})
# print('Количество видео (ожидается 1*10)', len(downloader.videos_info))
# pprint( downloader.videos_info)
# a = input()
# for  i in range(10):
#     print('#')
# print('Каналы видео из поиска(ожидается < 1*10)',len(downloader.channels_array))
# pprint(downloader.channels_array)
# a = input()
# for  i in range(10):
#     print('#')
# print('Каналы видео из комм',len(downloader.channels_of_comments_array))
# pprint(downloader.channels_of_comments_array)
