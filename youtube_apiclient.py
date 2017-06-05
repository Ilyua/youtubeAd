from apiclient.discovery import build
from apiclient.errors import HttpError

#РАзные кавычки!!!!

class ApiClient(object):
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    DEVELOPER_KEY = 'AIzaSyAOIfpRS2SDQftT3uiXn9s3UyffshfFd3Q'
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    SEARCH_MAX_PAGES = 1

    def get_videos_main_comments(self, video_id):
        try:
            results = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText'
            ).execute()
        except HttpError:
            results = {}
        video_comment_threads = results.get('items', [])
        if 'items' not in results:
            print('Warning: comment threads can\'t be got')

        for thread in video_comment_threads:
            yield thread


    def get_channel_info(self, channel_id):
        result = self.youtube.channels().list(
            part='snippet,contentOwnerDetails,statistics,localizations,status',
            id=channel_id
        ).execute()
        return result.get('items', [])


    def search_videos_by_key_phrase(self, phrase):
        page_token = None
        search_videos = []
        videos_info = []
        for _ in range(self.SEARCH_MAX_PAGES):
            search_response = self.youtube.search().list(
                q=phrase,
                type='video',
                part='id,snippet',
                maxResults=50,#max value allowed by youtube api
                pageToken=page_token
            ).execute()
            page_token = search_response.get('nextPageToken', None)
            for search_result in search_response.get('items', []):
                yield search_result['id']['videoId']
            if page_token == None:
                break


    def get_video_info(self, video_id):
        video_response = self.youtube.videos().list(
                id=video_id,
                part='snippet, recordingDetails'
            ).execute()
        return video_response.get('items', [])

