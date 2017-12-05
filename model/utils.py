#!/usr/bin/env python -*- coding: utf-8 -*-

import sys
import codecs
import pickle
from numpy import linalg, mean, dot, load
from gensim.models import LsiModel, keyedvectors

def print_lexical_scores(vocabulary, debiasing, neutral_word, vsm, score_function):
    if debiasing:
        if neutral_word not in vsm:
            print >> sys.stderr, "The neutral word is an OOV."
            sys.exit()
        neutral_bias = score_function(neutral_word)
    else:
        neutral_bias = 0

    score_dict = {}
    positive_normalizer = 0
    negative_normalizer = 0
    for line in codecs.open(vocabulary,'rb','utf8'):
        token = line.strip()
        if token and token in vsm:
            unbiased_formality = score_function(token) - neutral_bias
            score_dict[token] = unbiased_formality
            if unbiased_formality > positive_normalizer:
                positive_normalizer = unbiased_formality
            if -unbiased_formality > negative_normalizer:
                negative_normalizer = -unbiased_formality
    sys.stderr.write("Positive Normalizer: %f\n" % positive_normalizer)
    sys.stderr.write("Negative Normalizer: %f\n" % negative_normalizer)

    for token in score_dict:
        if score_dict[token] >= 0:
            print "%s\t%f" % (token.encode('utf8'),score_dict[token]/positive_normalizer)
        else:
            print "%s\t%f" % (token.encode('utf8'),score_dict[token]/negative_normalizer)

def read_lexical_scores(filename):
    lexical_scores = {}
    for line in codecs.open(filename,'rb','utf8'):
        segs = line.split()
        lexical_scores[segs[0]] = float(segs[1])
    return lexical_scores

def average_score(tokens, lexical_scores):
    textual_scores = []
    for token in tokens:
        if token in lexical_scores:
            textual_scores.append(lexical_scores[token])
    if len(textual_scores) > 0:
        return len(tokens),len(tokens)-len(textual_scores),mean(textual_scores)
    else:
        return len(tokens),len(tokens),None

def weighted_score(tokens, lexical_scores):
    textual_scores = []
    weight_sum = 0
    for token in tokens:
        if token in lexical_scores:
            textual_scores.append(abs(lexical_scores[token])*lexical_scores[token])
            weight_sum += abs(lexical_scores[token])
    if len(textual_scores) > 0:
        if weight_sum == 0:
            return len(tokens),len(tokens)-len(textual_scores),0
        else:
            return len(tokens),len(tokens)-len(textual_scores),sum(textual_scores)/weight_sum
    else:
        return len(tokens),len(tokens),None

def unitvec(vec):
    if vec.any():
        return vec/linalg.norm(vec)
    else:
        return vec

def normalize(x, alpha):
    return x/(alpha+abs(x))

class VSM:
    def __init__(self, name, model, components=None):
        if name == "lsa":
            self.vsm = LsiModel.load(model)
            self.vocab = self.vsm.id2word.token2id
            self.vector_size = self.vsm.num_topics
        elif name == "w2v":
            self.vsm = keyedvectors.KeyedVectors.load_word2vec_format(model, binary=True, unicode_errors='ignore')
            self.vocab = self.vsm.vocab
            self.vector_size = self.vsm.syn0.shape[1]
            # https://github.com/RaRe-Technologies/gensim/blob/master/gensim/models/keyedvectors.py
        elif name == "pickle":
            vsm_obj = pickle.load(open(model, "rb"))
            self.vsm = vsm_obj["vsm"]
            self.vocab = vsm_obj["map"]
            self.vector_size = self.vsm.shape[1]
        try:
            self.components = load(components)
        except (IOError, AttributeError):
            self.components = 1

    def __getitem__(self, word):
        if isinstance(self.vsm, LsiModel):
            return dot(self.components, self.vsm.projection.u[self.vocab[word]])
        elif isinstance(self.vsm, keyedvectors.KeyedVectors):
            return dot(self.components, self.vsm[word])
        else:
            return dot(self.components, self.vsm[self.vocab[word]])

    def __contains__(self, word):
        return word in self.vocab

    def cosine_similarity(self, w1, w2):
        return dot(unitvec(self[w1]), unitvec(self[w2]))

    def dot_product(self, w1, w2):
        return dot(self[w1], self[w2])

    def get_dict(self, words):
        dictionary = {}
        for word in words:
            dictionary[word] = self[word]
        return dictionary

    def get_array(self, words):
        array = []
        for word in words:
            array.append(self[word])
        return array
