from pprint import pprint
from downloader_class import Downloader

downloader = Downloader(1)

downloader.search_by_all_key_for_one_word(0)
downloader.search_by_all_key_for_one_word(1)

# downloader.create_channels_list(downloader.videos_info)
# downloader.create_channels_of_comments_list(downloader.videos_info)

print('Количество видео (ожидается 1*10)', len(downloader.videos_info))
pprint( downloader.videos_info)
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
