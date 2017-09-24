#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
from model import utils
from numpy import mean, sqrt, array
from scipy import stats
from itertools import izip

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--scores', required=True, help='lexical scores file')
    parser.add_argument('-f', '--file', required=True, help='evaluation file')
    parser.add_argument('-p', '--supplement', required=False, help='supplementary evaluation file')
    parser.add_argument('-t', '--type', required=True, help='evaluation type: masc, bean, ctrw')
    parser.add_argument('-m', '--method', required=False, type=str, default="weighted", \
                        help='sentence-scoring method: weighted, mean')
    parser.add_argument('-d', '--dedup', required=False, action="store_true", \
                        help='remove duplicate words in a sentence')
    args = parser.parse_args()
    
    lexical_scores = utils.read_lexical_scores(args.scores)
    
    if args.type == "masc" or args.type == "bean":
        total_words = 0
        total_sentences = 0
        uncovered_words = 0
        uncovered_sentences = 0
        scores_ref_valid = []
        scores_cal_valid = []
        with open(args.file,"rb") as file1, open(args.supplement,"rb") as file2:
            for line1, line2 in izip(file1, file2):
                segs = line1.split("\t")
                if not segs[1]:
                    continue
                total_sentences += 1
                tokens = line2.split()
                if args.dedup:
                    tokens = list(set(tokens))
                if args.method == "weighted":
                    v, oov, cal_score = utils.weighted_score(tokens, lexical_scores)
                elif args.method == "mean":
                    v, oov, cal_score = utils.average_score(tokens, lexical_scores)
                total_words += v
                uncovered_words += oov
                if cal_score != None:
                    ref_score = float(segs[0])
                    scores_ref_valid.append(ref_score)
                    scores_cal_valid.append(cal_score)
                else:
                    uncovered_sentences += 1
        print "uncovered: %d/%d | %d/%d" % (uncovered_sentences,total_sentences,uncovered_words,total_words)
        print "Spearman:  %.6f" % stats.spearmanr(scores_ref_valid, scores_cal_valid)[0]
        print "Pearson:   %.6f" % stats.pearsonr(scores_ref_valid, scores_cal_valid)[0]
        if args.type == "masc":
            scores_ref_norm = (array(scores_ref_valid)-50)/50
        elif args.type == "bean":
            scores_ref_norm = array(scores_ref_valid)/3
        print "RMSE:      %.6f" % sqrt(mean((scores_ref_norm-scores_cal_valid)**2))
    elif args.type == "ctrw":
        total = 0.0
        covered = 0.0
        correct = 0.0
        items = []
        with open(args.file,"rb") as filein:
            for line in filein:
                total += 1
                segs = line.split()
                if segs[0] in lexical_scores and segs[1] in lexical_scores:
                    covered += 1
                    # segs[1] is more formal
                    if lexical_scores[segs[0]] < lexical_scores[segs[1]]:
                        correct += 1
                    items.append((segs[0],segs[1],lexical_scores[segs[0]],lexical_scores[segs[1]]))
        print "coverage: %.6f | %d/%d" % (covered/total,covered,total)
        print "accuracy: %.6f | %d/%d" % (correct/covered,correct,covered)