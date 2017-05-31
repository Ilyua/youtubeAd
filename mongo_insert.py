import parser
from search_videos import youtube_search
import pymongo
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.youtube
film_dictionary = youtube_search(
    parser.search_dictionary_parser('5000lemma.txt'))


def insert_films_to_mongo(film_list):
    c_films = db.film
    c_films.insert(film_list)


def insert_comments_to_mongo(film_comments_list):
    c_comments = db.film_comments
    c_comments.insert(film_comments_list)


def insert_channels_to_mongo(channels_list):
    c_channels = db.channels
    c_channels.insert(channels_list)
