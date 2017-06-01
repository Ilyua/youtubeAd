import parser
from search_videos import youtube_searh

PAGES_NUMBER = 5
word_list = parser.search_dictionary_parser('5000lemma.txt')
dict = {}
for word in word_list:
    page_token = None
    for page_num in range(PAGES_NUMBER):
        dict+=youtube_search(word, page_token)#ddddddddddddddddddd
        page_token = dict["nextPagetoken"]#&&&


