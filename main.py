from pprint import pprint
from youtube_apiclient import ApiClient
from key_phrase_parser import parse_feq_dictionary
from pymongo import MongoClient
import sys
from datetime import datetime
import logging


client = MongoClient()
db = client.my_db
channels_coll = db.channels
videos_coll = db.videos
comments_coll = db.comments
subscriptions_coll = db.subscriptions
FORMAT = '%(asctime)s.%(msecs)d %(levelname)s : %(message)s'
logging.basicConfig(
    format=FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filename='./log/addys/{date}.log'.format(
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    )
)

def main(phrase,key):
    client = ApiClient(key)
    channel_ids = set()
    videos_ids = client.search_videos_by_key_phrase(phrase)

    for i,video_id in enumerate(videos_ids):
        logging.debug('Got video_id:{}'.format(video_id))
        for comment in client.get_videos_main_comments(video_id):
            try:
                authorChannelId = comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']

                logging.debug('Got authorChannelId:{}'.format(authorChannelId))

                channel_ids.update({authorChannelId})

                logging.debug('Start inserting comment by authorChannelId:{}'.format(authorChannelId))
                comments_coll.insert(comment)
                logging.debug('End inserting comment by authorChannelId:{}'.format(authorChannelId))
            except Exception as e:
                print('ERROR in main.py in channel_id block!!!')
                logging.error('On video: {video_id} - {problem}'.format(
                    video_id=video_id,
                    problem=(str(e))))




        logging.debug('Start inserting video by id:{}'.format(video_id))
        videos_coll.insert(client.get_video_info(video_id))
        logging.debug('End inserting video by id:{}'.format(video_id))

    for channel_id in channel_ids:
        logging.debug('Start inserting channel by id:{}'.format(channel_id))
        channels_coll.insert(client.get_channel_info(channel_id))
        logging.debug('End inserting channel by id:{}'.format(channel_id))

        for subscription in  client.get_channel_subscriptions(channel_id):

            if len(subscription) != 0:
                subscriptions_coll.insert(subscription)
                logging.debug('Sucesfull inserted subscriptions')
            else:
                logging.debug('No subscritions!')


























































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
