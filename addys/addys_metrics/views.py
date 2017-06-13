from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.my_db
videos = db.videos

def process_channel_id(request):
    if request.POST:
        channel_id = request.POST.get('channel_id')
        suscribers = db.videos.find()

        return HttpResponse(channel_id)

    return render(request, 'addys_metrics/process_channel_id_form.html')



