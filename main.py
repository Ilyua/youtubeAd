from pprint import pprint
from youtube_apiclient import ApiClient
from key_phrase_parser import parse_feq_dictionary

phrases_list = parse_feq_dictionary('5000lemma.txt')

client = ApiClient()
channel_ids = set()

for i, phrase in enumerate(phrases_list):
    if i >= 1:
        break
    videos = client.search_videos_by_key_phrase(phrase)


    for video_id in videos:
        channel_ids.update({comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            for comment in client.get_videos_main_comments(video_id)})


for id in channel_ids:
    pprint(client.get_channel_info(id))
    break

















































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
