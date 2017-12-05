#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
from numpy import dot, load

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-v', '--vocabulary', required=True, help='vocabulary file')
    parser.add_argument('-c', '--coefficient', required=True, help='coefficient vector')
    parser.add_argument('-d', '--debiasing', required=False, type=bool, default=False, help='debiasing: True/False')
    parser.add_argument('-e', '--neutral', required=False, default="at", help='neutral word')
    parser.add_argument('-s', '--similarity', required=False, default="cosine", help='similarity metric: cosine, dot')
    parser.add_argument('-i', '--incomponents', required=False, help='input subspace components (.npy)')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model, args.incomponents)
    u = load(args.coefficient)[0]
    
    if args.similarity == "cosine":
        utils.print_lexical_scores(args.vocabulary, args.debiasing, args.neutral, vsm, \
                                   lambda token: dot(u, utils.unitvec(vsm[token])))
    elif args.similarity == "dot":
        utils.print_lexical_scores(args.vocabulary, args.debiasing, args.neutral, vsm, \
                                   lambda token: dot(u, vsm[token]))