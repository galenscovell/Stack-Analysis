"""
WORD2VEC
=========
Basic implementation of a word2vec model.

@author GalenS <galen.scovell@gmail.com>
"""

import logging
import multiprocessing

import gensim


def pull_dataset(file_name):
    # Dataset must be a list of lists, sublists are tokenized words of a sentence
    data_set = []
    index = 0
    # Input file has one sentence per line
    # Clean well: remove all punctuation, non-ascii chars, stopwords, whitespace \n\t, etc.
    #   remove words that are entirely numbers (str.isdigit())
    #   lowercase, stem, set min size for a 'sentence' (5 words)
    with open(file_name, 'rb') as f:
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
        data_set,                            # 2D list of sentence words
        size=200,                            # Dimensionality of feature vectors
        window=3,                            # Context length around each word
        sg=1,                                # 0=CBOW, 1=skipgram
        min_count=100,                       # Min freq for a word to be considered
        alpha=0.025,                         # Initial learning rate, linearly drops to 0
        workers=multiprocessing.cpu_count(), # Parallelization workers
        max_vocab_size=None                  # Vocab size limit
    )
    # Save trained model to file
    model.save(name)


def load_model(name):
    # Load trained model file from current dir
    return gensim.models.Word2Vec.load(name)
