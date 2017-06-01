import re

def search_dictionary_parser(words_file_name):
    with open(words_file_name) as my_file:
        file_string = my_file.read()
    return re.findall(r'[а-я]+', file_string)
