#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import codecs
from model import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--scores', required=True, help='lexical scores file')
    parser.add_argument('-i', '--input', required=True, help='input file')
    parser.add_argument('-m', '--method', required=False, type=str, default="weighted", \
                        help='sentence-scoring method: weighted, mean')
    parser.add_argument('-d', '--dedup', required=False, action="store_true", \
                        help='remove duplicate words in a sentence')
    args = parser.parse_args()
    
    lexical_scores = utils.read_lexical_scores(args.scores)
    
    scores_ref_valid = []
    scores_cal_valid = []
    for line in codecs.open(args.input,'rb','utf8'):
        tokens = line.split()
        if args.dedup:
            tokens = list(set(tokens))
        if args.method == "weighted":
            v, oov, score = utils.weighted_score(tokens, lexical_scores)
        elif args.method == "mean":
            v, oov, score = utils.average_score(tokens, lexical_scores)
        if score == None:
            score = float('NaN')
        print "%.6f\t%s" % (score, line.encode('utf8').strip())