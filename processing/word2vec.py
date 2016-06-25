"""
WORD2VEC
=========
Basic implementation of a word2vec model.

@author GalenS <galen.scovell@gmail.com>
"""

import logging

import gensim


def pull_dataset(file_name):
    # Data set must be a list of lists, sub-lists are tokenized words of a sentence
    data_set = []
    index = 0
    # Input file has one sentence per line
    with open(file_name, 'r') as f:
        for line in f:
            if index % 1000 == 0:
                print('Loading dataset: {0}'.format(index))
            index += 1

            words = []
            line = line.rstrip().split(' ')
            for word in line:
                words.append(word)
            data_set.append(words)
    return data_set


def create_and_train_model(data_set, name):
    # Setup logging messages
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
    # Create and train word2vec model using given data_set
    model = gensim.models.Word2Vec(
        data_set,                             # 2D list of sentence words
        size=100,                             # Dimensionality of feature vectors
        window=5,                             # Context length around each word
        sg=1,                                 # 0=CBOW, 1=skipgram
        min_count=50,                         # Min freq for a word to be considered
        alpha=0.025,                          # Initial learning rate, linearly drops to 0
        workers=3,                            # Parallelization workers
        max_vocab_size=None                   # Vocab size limit
    )
    # Save trained model to file
    model.save(name)


def load_model(name):
    # Load trained model file from current dir
    return gensim.models.Word2Vec.load(name)


def search(model, positive=[], negative=[]):
    results = model.most_similar(positive=positive, negative=negative, topn=6)
    print('positive {0} | negative {1}'.format(positive, negative))
    for x in range(len(results)):
        print('{:>20}'.format(results[x][0]))
