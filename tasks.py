from celery import Celery
from apiclient.discovery import build
from apiclient.errors import HttpError
app = Celery('tasks', backend='amqp', broker='amqp://')

def make_youtube(developer_key):
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=developer_key)
    return youtube


@app.task(name='get_videos_main_comments')
def get_videos_main_comments(video_id,developer_key):
    try:
        result = make_youtube(developer_key).commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        ).execute()
    except HttpError:
        result = {}
    return result


@app.task(name='get_channel_info')
def get_channel_info(channel_id,developer_key):
    result = make_youtube(developer_key).channels().list(
        part='snippet,contentOwnerDetails,statistics,localizations,status',
        id=channel_id
    ).execute()
    return result


@app.task(name='search_videos_by_key_phrase')
def search_videos_by_key_phrase(page_token, phrase,developer_key):
    result = make_youtube(developer_key).search().list(
        q=phrase,
        type='video',
        part='id,snippet',
        maxResults=50,  # max value allowed by youtube api is 50
        pageToken=page_token,
        regionCode='RU'
    ).execute()
    return result


@app.task(name='get_video_info')
def get_video_info(video_id,developer_key):
    result = make_youtube(developer_key).videos().list(
        id=video_id,
        part='snippet, recordingDetails'
    ).execute()
    return result
