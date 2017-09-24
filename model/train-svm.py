#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import codecs
import utils
from sklearn import svm, metrics
from sklearn.externals import joblib
from numpy import stack, concatenate, zeros, ones

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-p', '--positive', required=True, help='positive word seeds file')
    parser.add_argument('-n', '--negative', required=True, help='negative word seeds file')
    parser.add_argument('-s', '--svm', required=True, help='output SVM model')
    parser.add_argument('-k', '--kernel', required=False, default="linear", help='kernel: linear, rbf, cosine')
    parser.add_argument('-c', '--components', required=False, help='subspace components (.npy)')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model, args.components)
    positive_words = set(line.strip() for line in codecs.open(args.positive,'rb','utf8') if line.strip() in vsm)
    negative_words = set(line.strip() for line in codecs.open(args.negative,'rb','utf8') if line.strip() in vsm)
    
    vsm_array = vsm.get_array(list(positive_words)+list(negative_words))
    X = stack(vsm_array)
    y = concatenate([ones(len(positive_words)), zeros(len(negative_words))])

    if args.kernel == "cosine":
        svm_model = svm.SVC(kernel=metrics.pairwise.cosine_similarity).fit(X, y)
    else:
        svm_model = svm.SVC(kernel=args.kernel).fit(X, y)

    yh = svm_model.decision_function(X)
    print "Training accuracy: %f" % svm_model.score(X, y)
    joblib.dump(svm_model, args.svm)