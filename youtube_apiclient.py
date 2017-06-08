

import tasks
# РАзные кавычки!!!!


class ApiClient(object):
    SEARCH_MAX_PAGES = 1

    def __init__(self, developer_key):
        self.developer_key = developer_key


    def get_videos_main_comments(self, video_id):
        results = tasks.get_videos_main_comments.delay(video_id,self.developer_key).get()
        if 'items' not in results:
            print('Warning: comment threads can\'t be got')
        video_comment_threads = results.get('items', [])
        if len(video_comment_threads) == 0:
            return []
        for thread in video_comment_threads:
            yield thread


    def get_channel_info(self, channel_id):
        result = tasks.get_channel_info.delay(channel_id, self.developer_key).get()
        return result.get('items', [])


    def search_videos_by_key_phrase(self, phrase):
        page_token = None
        search_videos = []
        videos_info = []
        for _ in range(self.SEARCH_MAX_PAGES):
            search_response = tasks.search_videos_by_key_phrase.delay(page_token,phrase.decode(),self.developer_key).get()
            page_token = search_response.get('nextPageToken', None)
            for search_result in search_response.get('items', []):
                yield search_result['id']['videoId']
            if page_token is None:
                break


    def get_video_info(self, video_id):

        video_response = tasks.get_video_info.delay(video_id,self.developer_key).get()

        return video_response.get('items', [])


