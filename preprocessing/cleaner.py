"""
CLEANER
=========
Handles cleaning steps for transforming JSON map contents into usable format
for word2vec and/or topic modeling.

@author GalenS <galen.scovell@gmail.com>
"""

import string
import sys

import nltk
from bs4 import BeautifulSoup
from nltk.collocations import *
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import PorterStemmer

punc = string.punctuation + '\n\r\t'
stop = stopwords.words('english')

bigram_measures = nltk.collocations.BigramAssocMeasures()
p_stemmer = PorterStemmer()


def get_cleaned_sentences(text):
    text = ''.join(i for i in text if ord(i) < 128)  # Remove non-ASCII characters
    text = text.replace('\r', '. ').replace('\n', '. ').replace('\t', ' ')
    text = text.replace('  ', ' ').replace('..', '.').lower()
    sentences = nltk.sent_tokenize(text)
    return sentences


def get_stemmed(words):
    stemmed_words = [p_stemmer.stem(word) for word in words]
    return stemmed_words


def get_bigrams(words, n):
    finder = BigramCollocationFinder.from_words(words)
    raw_bigrams = finder.nbest(bigram_measures.pmi, n)
    bigrams = ['_'.join(bigram) for bigram in raw_bigrams]
    return bigrams


def for_word2vec(content, out_path):
    idx = 0
    total = len(content)
    cleaned = []

    for entry in content:
        body = content[entry]['body']

        if idx % 1000 == 0:
            print('{0} / {1}'.format(idx, total))
        idx += 1

        # Remove all html tags, preserving space between entries
        soup = BeautifulSoup(body, 'lxml')
        soup = ' '.join(soup.findAll(text=True))

        sentences = get_cleaned_sentences(soup)
        for sentence in sentences:
            result = []
            for p in punc:
                sentence = sentence.replace(p, '')
            words = sentence.rstrip().split(' ')
            for word in words:
                word = word.rstrip()
                if word not in stop and not word.isdigit() and wordnet.synsets(word):
                    result.append(word)
            if len(result) > 5:
                cleaned.append(' '.join(result))

    save(cleaned, out_path)


def for_topic_modeling(content):
    idx = 0
    total = len(content)
    cleaned = []

    # for entry in content:
    #     body = content[entry]['body']
    #
    #     if idx % 1000 == 0:
    #         print('{0} / {1}'.format(idx, total))
    #     idx += 1
    #
    #     # Remove all html tags, preserving space between entries
    #     soup = BeautifulSoup(body, 'lxml')
    #     soup = ' '.join(soup.findAll(text=True))
    #
    #     sentences = get_cleaned_sentences(soup)
    #     for sentence in sentences:
    #         result = []
    #         for p in punc:
    #             sentence = sentence.replace(p, '')
    #         words = sentence.rstrip().split(' ')
    #         for word in words:
    #             word = word.rstrip()
    #             if word not in stop and not word.isdigit() and wordnet.synsets(word):
    #                 result.append(word)
    #         if len(result) > 5:
    #             cleaned.append(' '.join(result))
    return cleaned


def save(contents, out_path):
    with open(out_path, 'w') as f:
        for c in contents:
            f.write(c + '\n')
