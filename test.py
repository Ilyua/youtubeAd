import pymongo
import re
from pprint import pprint
from pymongo import MongoClient
from apiclient.discovery import build
from apiclient.errors import HttpError
from collections import Counter
client = MongoClient('localhost', 27017)
db = client.my_db
videos = db.videos
subscriptions = db.subscriptions
channel_id = 'UCrFiA0hztL9e8zTi_qBuW4w'
key = 'AIzaSyBdBmRWp_mYe1SW6HRpdWeN_-ju_cvkAgk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
developerKey=key)
cursor_of_my_s = db.subscriptions.find({'snippet.resourceId.channelId': channel_id},{'snippet.channelId':1,'_id':0})
ids_of_my_s = [i['snippet']['channelId'] for i in cursor_of_my_s]
#print(len(ids_of_my_s))
#получили айди своей подписоты
subcr_of_my_s = []

tags = []
for i in ids_of_my_s[:10]:
    #print(db.subscriptions.find({'snippet.channelId': i}))
    cursor_of_all_subscr = db.subscriptions.find({'snippet.channelId': i})
    #pprint(cursor_of_all_subscr.count())
    #получили все подписки одного подписчика
    channels_ids_of_one_subscr = [i['snippet']['resourceId']['channelId'] for i in cursor_of_all_subscr]
    print(len(channels_ids_of_one_subscr))
    #pprint(channels_ids_of_one_subscr)
    for channel_id in channels_ids_of_one_subscr[:10]:
        result = youtube.channels().list(
        part='topicDetails',
        id=channel_id
        ).execute()
        result = result.get('items',[])[0]
        channel_categor = result.get('topicDetails',{}).get('topicCategories',[])
        #pprint(channel_categor)
        for category_link in channel_categor:
            tags.append(re.split(r'/', category_link)[-1])

pprint(Counter(tags).most_common(10))

