#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import codecs
import utils
from sklearn.decomposition import PCA
from sklearn.utils import shuffle
from numpy import save

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help='gensim LSA or word2vec binary model')
    parser.add_argument('-t', '--type', required=True, help='model type: lsa, w2v')
    parser.add_argument('-p', '--pairs', required=True, help='word pairs file')
    parser.add_argument('-r', '--ratio', required=False, type=float, default=1.0, help='sample ratio')
    parser.add_argument('-k', '--number', required=False, type=int, default=10, help='number of components to keep')
    parser.add_argument('-c', '--components', required=True, help='output principal components')
    parser.add_argument('-s', '--similarity', required=False, default="cosine", help='similarity metric: cosine, dot')
    args = parser.parse_args()
    
    vsm = utils.VSM(args.type, args.model)
    words = set()
    pair_dist = {}
    for line in codecs.open(args.pairs,'rb','utf8'):
        segs = line.strip().split("\t")
        if (segs[0],segs[1]) not in pair_dist and segs[0] in vsm and segs[1] in vsm:
            dist = vsm[segs[0]] - vsm[segs[1]]
            pair_dist[(segs[0],segs[1])] = dist
            pair_dist[(segs[1],segs[0])] = -dist
            words.add(segs[0])
            words.add(segs[1])
    print "%d distinct pairs were found (%d word types)." % (len(pair_dist)/2,len(words))
    
    if args.similarity == "cosine":
        for key in pair_dist.iterkeys():
            pair_dist[key] = utils.unitvec(pair_dist[key])
    
    pca = PCA(n_components=args.number)
    pca.fit(shuffle(pair_dist.values(), n_samples=int(len(pair_dist)*args.ratio)))
    print('explained variance ratio: %s' % str(pca.explained_variance_ratio_))
    
    save(args.components, pca.components_)