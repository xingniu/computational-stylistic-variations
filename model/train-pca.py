#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import codecs
import utils
from sklearn.decomposition import PCA
from sklearn.utils import shuffle
from numpy import stack, dot, save

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-p', '--positive', required=True, help='positive word seeds file')
    parser.add_argument('-n', '--negative', required=True, help='negative word seeds file')
    parser.add_argument('-r', '--ratio', required=False, type=float, default=1.0, help='sample ratio')
    parser.add_argument('-k', '--number', required=False, type=int, default=10, help='number of components to keep')
    parser.add_argument('-c', '--components', required=True, help='output principal components')
    parser.add_argument('-s', '--similarity', required=False, default="cosine", help='similarity metric: cosine, dot')
    parser.add_argument('-i', '--incomponents', required=False, help='input subspace components (.npy)')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model, args.incomponents)
    positive_words = set(line.strip() for line in codecs.open(args.positive,'rb','utf8') if line.strip() in vsm)
    negative_words = set(line.strip() for line in codecs.open(args.negative,'rb','utf8') if line.strip() in vsm)
    vsm_array = vsm.get_array(list(positive_words)+list(negative_words))
    X = stack(vsm_array)
    
    if args.similarity == "cosine":
        for i in xrange(X.shape[0]):
            X[i] = utils.unitvec(X[i])
    
    pca = PCA(n_components=args.number)
    pca.fit(shuffle(X, n_samples=int(len(vsm_array)*args.ratio)))
    print('explained variance ratio: %s' % str(pca.explained_variance_ratio_))
    
    for i in xrange(args.number):
        postive_sum = 0
        for x in X[0:len(positive_words)]:
            postive_sum += dot(pca.components_[i], x)
        if postive_sum < 0:
            pca.components_[i] = -pca.components_[i]
    
    save(args.components, pca.components_)