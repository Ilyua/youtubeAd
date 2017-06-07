from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://')
from apiclient.discovery import build
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SEARCH_MAX_PAGES = 1
dev_key = "AIzaSyBdBmRWp_mYe1SW6HRpdWeN_-ju_cvkAgk"
youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=dev_key)

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

@app.task(name='get_videos_main_comments')
def get_videos_main_comments(video_id):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    ).execute()
    return request


@app.task(name='get_channel_info')
def get_channel_info(channel_id):
    request = youtube.channels().list(
        part='snippet,contentOwnerDetails,statistics,localizations,status',
        id=channel_id
    ).execute()
    return request

@app.task(name='search_videos_by_key_phrase')
def search_videos_by_key_phrase(page_token, phrase):
    request = youtube.search().list(
        q=phrase,
        type='video',
        part='id,snippet',
        maxResults=50,  # max value allowed by youtube api is 50
        pageToken=page_token,
        regionCode='RU'
    ).execute()
    return request


@app.task(name='get_video_info')
def get_video_info(video_id):
    request = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails'
    ).execute()
    return request

