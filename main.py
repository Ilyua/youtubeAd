from pprint import pprint
from downloader_class import Downloader

downloader = Downloader(2)

downloader.search_by_all_key()
pprint(downloader.videos_info)
downloader.create_channels_list(downloader.videos_info)
#pprint(downloader.channels_array)
