import parser
from search_videos import youtube_search
import pprint

PAGES_NUMBER = 10
word_list = parser.search_dictionary_parser('5000lemma.txt')
dict = {}
# for word in word_list:
word = word_list[0]

dict = youtube_search(word, PAGES_NUMBER)  # ddddddddddddddddddd
# pprint.pprint(dict[len(dict)-1])


# pprint.pprint(dict)
