#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import codecs
import utils
from numpy import mean

def similarity_diff(word, positive_words, negative_words, vsm, similarity_metric):
    if similarity_metric == "cosine":
        positive_score = mean([vsm.cosine_similarity(word,w) for w in positive_words])
        negative_score = mean([vsm.cosine_similarity(word,w) for w in negative_words])
    elif similarity_metric == "dot":
        positive_score = mean([vsm.dot_product(word,w) for w in positive_words])
        negative_score = mean([vsm.dot_product(word,w) for w in negative_words])
    return positive_score - negative_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-p', '--positive', required=True, help='positive word seeds file')
    parser.add_argument('-n', '--negative', required=True, help='negative word seeds file')
    parser.add_argument('-v', '--vocabulary', required=True, help='vocabulary file')
    parser.add_argument('-d', '--debiasing', required=False, type=bool, default=True, help='debiasing: True/False')
    parser.add_argument('-e', '--neutral', required=False, default="at", help='neutral word')
    parser.add_argument('-s', '--similarity', required=False, default="cosine", help='similarity metric: cosine, dot')
    parser.add_argument('-c', '--components', required=False, help='subspace components (.npy)')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model, args.components)
    positive_words = set(line.strip() for line in codecs.open(args.positive,'rb','utf8') if line.strip() in vsm)
    negative_words = set(line.strip() for line in codecs.open(args.negative,'rb','utf8') if line.strip() in vsm)
    
    utils.print_lexical_scores(args.vocabulary, args.debiasing, args.neutral, vsm, \
                               lambda token: similarity_diff(token, positive_words, negative_words, vsm, args.similarity))