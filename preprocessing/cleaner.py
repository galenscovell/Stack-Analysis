"""
CLEANER
=========
Handles cleaning steps for transforming JSON map contents into usable format
for word2vec, markov chains or topic modeling.

@author GalenS <galen.scovell@gmail.com>
"""

import re
import string

import nltk
from bs4 import BeautifulSoup
from nltk.collocations import *
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import PorterStemmer

whitespace = '\n\r\t'
normal_punc = string.punctuation + whitespace
stop = stopwords.words('english')

# For markov chain
mc_blacklist = '"#%()$*/<=>@[\]^_`{|}~:' + whitespace
mc_whitelist = ('--', ',')
mc_end_punc = ('.', '...', '!', '?', ';')
mc_total_whitelist = mc_whitelist + mc_end_punc

bigram_measures = nltk.collocations.BigramAssocMeasures()
p_stemmer = PorterStemmer()


def get_cleaned_sentences(text):
    text = ''.join(i for i in text if ord(i) < 128)  # Remove non-ASCII characters
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


def start_clean(content, out_path):
    idx = 0
    total = len(content)
    cleaned = []
    non_words = {}

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
            for_markov_chain(cleaned, non_words, sentence)

    save(cleaned, out_path)


def for_markov_chain(cleaned, non_words, sentence):
    for p in mc_blacklist:
        sentence = sentence.replace(p, '')
    # Split out words from sentence on space or .,!?;
    # Preserve '- within words
    words = re.findall(r"[\w'-]+|[.,!?;]", sentence.strip())

    current_sentence = []
    for word in words:
        word = word.strip()
        if len(word) > 0:
            if word in mc_end_punc:
                current_sentence.append(word)
                finalize_markov_result(cleaned, current_sentence)
                current_sentence = []
            if word in mc_whitelist or word in stop or wordnet.synsets(word):
                current_sentence.append(word)
            else:
                if word in non_words:
                    non_words[word] += 1
                else:
                    non_words[word] = 1
                # If 'non-word' has been seen more than 10 times, add it as regular word
                if non_words[word] > 10:
                    current_sentence.append(word)

    # Finalize remaining leftover parsed sentence
    finalize_markov_result(cleaned, current_sentence)


def finalize_markov_result(cleaned, result):
    # If there are at least 5 words in the sentence...
    # If first 'word' is punctuation, remove it
    # Capitalize first word
    # If last 'word' is comma, replace it with period
    # If last 'word' is not in punc whitelist, add period
    if len(result) > 5:
        if result[0] in mc_total_whitelist:
            result.remove(result[0])
        result[0] = result[0].capitalize()
        if result[-1] in (',', ';'):
            result[-1] = '.'
        if result[-1] not in mc_end_punc:
            result.append('.')

        cleaned.append('START-MC NOW-MC ' +
                       ''.join(w if w in mc_total_whitelist else ' ' + w for w in result).strip() +
                       ' END-MC')


def for_word2vec(cleaned, non_words, sentence):
    result = []
    for p in normal_punc:
        sentence = sentence.replace(p, '')
    words = sentence.strip().split(' ')
    for word in words:
        word = word.strip()
        if len(word) > 0 and word not in stop and not word.isdigit():
            if not wordnet.synsets(word):
                if word in non_words:
                    non_words[word] += 1
                else:
                    non_words[word] = 1

                if non_words[word] > 10:
                    result.append(word)
            else:
                result.append(word)

    if len(result) > 5:
        cleaned.append(' '.join(result))


def for_topic_modeling(content, out_path):
    return


def save(contents, out_path):
    with open(out_path, 'w') as f:
        for c in contents:
            f.write(c + '\n')
