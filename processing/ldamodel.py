"""
LDA TOPIC MODELING
===================
Basic implementation of an LDA topic model.

@author GalenS <galen.scovell@gmail.com
"""

import logging

import gensim


def load_data_set(file_name):
    data_set = []
    with open(file_name, 'r') as f:
        for line in f:
            cleaned = []
            words = line.lower().rstrip().split(' ')
            for word in words:
                cleaned.append(word)
            data_set.append(cleaned)

    term_dict = gensim.corpora.Dictionary(data_set)
    corpus = [term_dict.doc2bow(data) for data in data_set]
    return term_dict, corpus


def create_and_train_model(term_dict, corpus, name):
    # Setup logging messages
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
    # Create and train LDA topic model using given term_dict and corpus
    model = gensim.models.LdaMulticore(
        corpus=corpus,       # Corpus
        num_topics=300,      # Number of topics to generate
        id2word=term_dict,   # Map for id (int) to word (string)
        passes=20,           # Iterations over corpus, higher is more accurate but slower
        workers=4            # Parallelized workers
    )
    model.save(name)


def load_model(name):
    # Load trained model file from current dir
    return gensim.models.LdaModel.load(name)
