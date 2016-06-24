"""
MAIN ENTRY
===========
Primary entry point for application.

@author GalenS <galen.scovell@gmail.com>
"""

import os

from util import map_handler
from preprocessing import parse_xml
from preprocessing import cleaner


if __name__ == '__main__':
    os.chdir(r'C:\Users\Galen\Documents\GitHub\Stack-Analysis')

    # parse_xml.from_tags(r'datasets/travel.stackexchange.com/Tags.xml')
    # parse_xml.from_posts(r'datasets/travel.stackexchange.com/Posts.xml')

    # map_handler.pretty_print_json(r'datasets/travel.stackexchange.com/Tags.json')
    # map_handler.pretty_print_json(r'datasets/travel.stackexchange.com/Posts.json')

    posts = map_handler.load_json(r'datasets/travel.stackexchange.com/Posts.json')
    cleaner.for_word2vec(posts, r'datasets/travel.stackexchange.com/Posts.txt')
