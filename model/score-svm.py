#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import utils
from sklearn.externals import joblib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-v', '--vocabulary', required=True, help='vocabulary file')
    parser.add_argument('-s', '--svm', required=True, help='SVM model')
    parser.add_argument('-d', '--debiasing', required=False, type=bool, default=False, help='debiasing: True/False')
    parser.add_argument('-e', '--neutral', required=False, default="at", help='neutral word')
    parser.add_argument('-c', '--components', required=False, help='subspace components (.npy)')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model, args.components)
    svm_model = joblib.load(args.svm)
    
    utils.print_lexical_scores(args.vocabulary, args.debiasing, args.neutral, vsm, \
                               lambda token: svm_model.decision_function(vsm[token].reshape(1, -1)))