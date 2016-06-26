"""
MAIN ENTRY
===========
Primary entry point for application.

@author GalenS <galen.scovell@gmail.com>
"""

import os

from preprocessing import cleaner
from preprocessing import parse_xml
from processing import markov_chain
from processing import word2vec
from util import map_handler


def create_json_maps(topic):
    resource = r'datasets/{0}.stackexchange.com/'.format(topic)

    parse_xml.from_tags(resource + 'Tags.xml')
    parse_xml.from_posts(resource + 'Posts.xml')

    # parse_xml.from_post_history(resource + 'PostHistory.xml')
    # map_handler.pretty_print_json(resource + 'PostHistory.json')


def create_model_dataset(topic, target):
    resource = r'datasets/{0}.stackexchange.com/'.format(topic)

    posts = map_handler.load_json(resource + 'Posts.json')
    # post_history = map_handler.load_json(resource + 'PostHistory.json')

    if target == 'lda':
        cleaner.for_topic_modeling(posts, resource + 'Posts_lda.txt')
    elif target == 'word2vec':
        cleaner.for_word2vec(posts, resource + 'Posts_word2vec.txt')
    else:
        cleaner.start_clean(posts, resource + 'Posts_markov_chain.txt')


def search_word2vec(model, topics):
    print('{:>20}'.format('gaming'))

    word2vec.search(model, positive=[topics[0]])
    word2vec.search(model, positive=[topics[1]])
    word2vec.search(model, positive=[topics[0], topics[1]])
    word2vec.search(model, positive=[topics[0]], negative=[topics[1]])
    word2vec.search(model, positive=[topics[1]], negative=[topics[0]])



if __name__ == '__main__':
    os.chdir(r'C:\Users\Galen\Documents\GitHub\Stack-Analysis')

    topic = 'travel'

    # create_json_maps(topic)
    # create_model_dataset(topic, 'markov_chain')

    markov_chain.run(topic, 8, False)

    # word2vec.create_and_train_model(word2vec_set, 'gaming_word2vec_model_sg')
    # model = word2vec.load_model('gaming_word2vec_model_sg')
    # search_word2vec(model, ['dark', 'souls'])
