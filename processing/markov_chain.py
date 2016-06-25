"""
MARKOV CHAIN
=============
Used markov chains to randomly generate sentences.

@author GalenS <galen.scovell@gmail.com>
"""

import pickle
import random
import re

mc_whitelist = ('.', '...', '!', ',', '?', ';')


def generate_trigram(words):
    if len(words) < 3:
        return
    for i in range(len(words) - 2):
        yield (words[i], words[i + 1], words[i + 2])


def create_chain(words):
    d = {}
    for word1, word2, word3 in generate_trigram(words):
        key = (word1, word2)
        if key in d:
            d[key].append(word3)
        else:
            d[key] = [word3]
    return d


def generate_sentence(chain, sword1='START-MC', sword2='NOW-MC'):
    new_sentence = []
    while True:
        sword1, sword2 = sword2, random.choice(chain[(sword1, sword2)])
        if sword2 == 'END-MC':
            break
        new_sentence.append(sword2)

    return ''.join(w if w in mc_whitelist else ' ' + w for w in new_sentence).strip()


def generate_paragraph(chain, n):
    new_sentences = []

    for x in range(n):
        if len(new_sentences) > 0:
            print(new_sentences[-1])
            last_sentence = re.findall(r"[\w']+|[.,!?;]", new_sentences[-1].strip())
            print(last_sentence)
            new_sentences.append(generate_sentence(chain, 'NOW-MC', last_sentence[-2]))
        else:
            new_sentences.append(generate_sentence(chain))

    for sentence in new_sentences:
        print(sentence)


def create_pickle(topic):
    source = r'datasets/{0}.stackexchange.com/Posts_markov_chain.txt'.format(topic)

    print('Reading dataset...')
    words = []
    with open(source, 'r') as f:
        idx = 0
        for line in f:
            if idx % 10000 == 0:
                print(idx)
            idx += 1
            sentence_words = re.findall(r"[\w'-]+|[.,!?;]", line.strip())
            words.extend(sentence_words)

    print('Constructing chain...')
    chain = create_chain(words)

    print('Outputting pickle...')
    with open('{0}_markov_chain.pickle'.format(topic), 'wb') as f:
        pickle.dump(chain, f)



def run(topic, n, generate=True):
    if generate:
        create_pickle(topic)

    with open('{0}_markov_chain.pickle'.format(topic), 'rb') as pf:
        word_chain = pickle.load(pf)

    print('\nSeparate sentences:')
    for x in range(n):
        print(generate_sentence(word_chain))

    # print('\nOne paragraph:')
    # generate_paragraph(word_chain, n)
