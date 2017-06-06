import re


def parse_feq_dictionary(file_name):
    REGEX = re.compile(
        '(?P<num>\d+) (?P<freq>[\d\.]+) (?P<phrase>[^ ]+) (?P<type>[a-zA-Z]+)')
    with open(file_name, 'r') as my_file:
        for nline, line in enumerate(my_file.readlines()):
            match = REGEX.match(line)

            if match is None:
                raise Exception('Problem with format in file {} (line {})'.format(
                    file_name, nline))

            yield match.group('phrase')
