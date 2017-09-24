#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import logging
from gensim import corpora, models, matutils
from numpy import dot, mean

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TextCorpus(object):
    def __init__(self, filename):
        self.filename = filename
    
    def __iter__(self):
        for line in open(self.filename,"rb"):
            line = line.strip()
            if line:
                if line == "---":
                    document = ""
                else:
                    document += " "+line
            elif document:
                yield document.lower().split()

class Corpus(object):
    def __init__(self, corpus_file, words_file, threshold):
        self.text_corpus = TextCorpus(corpus_file)
        self.__build_dictionary(words_file, threshold)
        
    def __iter__(self):
        for doc in self.text_corpus:
            yield self.dictionary.doc2bow(doc)

    def __build_dictionary(self, words_file, threshold):
        self.dictionary = corpora.Dictionary(self.text_corpus, prune_at=None)
        good_ids = []
        for line in open(words_file,"rb"):
            segs = line.split("\t")
            if int(segs[1]) >= threshold:
                token = segs[0] if isinstance(segs[0], unicode) else unicode(segs[0], 'utf-8')
                if token in self.dictionary.token2id:
                    good_ids.append(self.dictionary.token2id[token])
        self.dictionary.filter_tokens(good_ids=good_ids)
        
def dot_product(word1, word2, lsi):
    vec1 = lsi.projection.u[lsi.id2word.token2id[word1]]
    vec2 = lsi.projection.u[lsi.id2word.token2id[word2]]
    return dot(matutils.unitvec(vec1), matutils.unitvec(vec2))
        
def raw_formality(word, formal_words, informal_words, lsi):
    formal_score = mean([dot_product(word,w,lsi) for w in formal_words])
    informal_score = mean([dot_product(word,w,lsi) for w in informal_words])
    return formal_score - informal_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--corpus', required=True, help='corpus file')
    parser.add_argument('-w', '--words', required=True, help='lowercased word count file')
    parser.add_argument('-m', '--model', required=True, help='output model file')
    parser.add_argument('-t', '--threshold', required=False, type=int, default=5, help='threshold')
    parser.add_argument('-d', '--dimension', required=False, type=int, default=20, help='dimension')
    args = parser.parse_args()
     
    corpus = Corpus(args.corpus, args.words, args.threshold)
    tfidf = models.TfidfModel(corpus)
    lsi = models.LsiModel(tfidf[corpus], id2word=corpus.dictionary, num_topics=args.dimension)
    lsi.save(args.model)