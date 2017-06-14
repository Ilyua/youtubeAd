from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import pymongo
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.my_db
videos = db.videos
subscriptions = db.subscriptions

def process_channel_id(request):
    if request.POST:
        channel_id= request.POST.get('channel_id')

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
        #channel_id = 'UCrFiA0hztL9e8zTi_qBuW4w'
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

        #pprint(Counter(tags).most_common(10))




        context = {'subscr_count':cursor_of_my_s.count(),'subscr':str(Counter(tags).most_common(10))}


        #return HttpResponse(subscribers    )
        return render(request, 'addys_metrics/process_channel_id_form.html',context)

    return render(request, 'addys_metrics/process_channel_id_form.html')






 #subscribers_of_my_channel = db.subscriptions.find({'snippet.resourceId.channelId': channel_id})
        # channels_ids_of_my_subscr = db.subscriptions.find({'snippet.resourceId.channelId': channel_id},{'snippet.channelId':1,'_id':0})
        # channels_id_list_of_my_auditory = [i['snippet']['channelId'] for i in channels_ids_of_my_subscr]
        # subscriptions_of_your_auditory = []
        # for i in channels_id_list:
        #     for subscriptions in db.subscriptions.find({'snippet.channelId': i})
        #         subscription_of_your_auditory.append(subscriptions)
        # channels_ids_of_my_auditory = [i['snippe0t']['resourceId']['channelId'] for i in subscription_of_your_auditory ]
        # interests_of_your_auditory = db.channels
