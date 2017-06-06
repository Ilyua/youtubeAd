

from pymongo import MongoClient
client = MongoClient()
db = client.my_db

channels_coll = db.channels
videos_coll = db.videos
comments_coll = db.comments

for video in
channels_coll.insert(channel)
videos_coll.insert(video)
comments_coll.insert(video)
