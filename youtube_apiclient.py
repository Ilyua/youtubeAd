import tasks
import pprint


class ApiClient(object):
    PHRASE_SEARCH_MAX_PAGES = 1
    SUBSCR_SEARCH_MAX_PAGES = 100

    def __init__(self, developer_key):
        self.developer_key = developer_key


    def get_videos_main_comments(self, video_id):
        vid_main_comm_response = tasks.get_videos_main_comments.delay(video_id,self.developer_key).get()
        if 'items' not in vid_main_comm_response:
            print('Warning: comment threads can\'t be got')
        video_comment_threads = vid_main_comm_response.get('items', [])
        if len(video_comment_threads) == 0:
            return []
        for thread in video_comment_threads:
            yield thread


    def get_channel_info(self, channel_id):
        channel_info_response = tasks.get_channel_info.delay(channel_id, self.developer_key).get()
        return channel_info_response.get('items', [])


    def search_videos_by_key_phrase(self, phrase):
        page_token = None
        search_videos = []
        videos_info = []
        for _ in range(self.PHRASE_SEARCH_MAX_PAGES):
            search_response = tasks.search_videos_by_key_phrase.delay(page_token,phrase.decode(),self.developer_key).get()
            page_token = search_response.get('nextPageToken', None)
            for search_result in search_response.get('items', []):
                yield search_result['id']['videoId']
            if page_token is None:
                break


    def get_video_info(self, video_id):
        video_response = tasks.get_video_info.delay(video_id,self.developer_key).get()
        return video_response.get('items', [])

    def get_channel_subscriptions(self, channel_id):
        page_token =  None
        for _ in range(self.SUBSCR_SEARCH_MAX_PAGES):
            subscribers_response = tasks.get_channel_subscriptions.delay(page_token,channel_id,self.developer_key).get()
            page_token = subscribers_response.get('nextPageToken', None)


            for search_result in subscribers_response.get('items', []):
                yield search_result
            if page_token is None:
                break


