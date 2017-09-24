#!/usr/bin/env python -*- coding: utf-8 -*-

import argparse
import zipfile
from collections import defaultdict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--style', required=True, help='style_annotations.zip file')
    parser.add_argument('-f', '--formality', required=False, help='Formality_Word_Lists.zip file')
    parser.add_argument('-o', '--operation', required=False, default="self", help='Operation: self, union, diff')
    parser.add_argument('-t', '--type', required=True, help='Type: formal, informal, neutral')
    args = parser.parse_args()
    
    literary_words = defaultdict(int)
    objective_words = defaultdict(int)
    colloquial_words = defaultdict(int)
    all_words = set()
    
    with zipfile.ZipFile(args.style, "r") as zipf:
        for name in zipf.namelist():
            if name.endswith(".csv"):
                for line in zipf.open(name):
                    segs = line.strip().split(",")
                    if segs[0] and segs[0] != "word":
                        if segs[1]:
                            literary_words[segs[0]] += 1
                        if segs[3]:
                            objective_words[segs[0]] += 1
                        if segs[4]:
                            colloquial_words[segs[0]] += 1
                        all_words.add(segs[0])
                        
    formal_seeds = set()
    informal_seeds = set()
    if args.formality:
        with zipfile.ZipFile(args.formality, "r") as zipf:
            for name in zipf.namelist():
                if name == "formal_seeds_100.txt":
                    for line in zipf.open(name):
                        formal_seeds.add(line.strip())
                elif name == "informal_seeds_100.txt":
                    for line in zipf.open(name):
                        informal_seeds.add(line.strip())
    
    strong_literary_words = set(w for w in literary_words if literary_words[w] >= 3)
    strong_objective_words = set(w for w in objective_words if objective_words[w] >= 3)
    strong_colloquial_words = set(w for w in colloquial_words if colloquial_words[w] >= 3)
    
    strong_formal_words = strong_literary_words.union(strong_objective_words)
    neutral_words = all_words.difference(literary_words.iterkeys()) \
                             .difference(objective_words.iterkeys()) \
                             .difference(colloquial_words.iterkeys())
    
    if args.operation == "self":
        if args.type == "formal":
            for word in strong_formal_words:
                print word
        elif args.type == "informal":
            for word in strong_colloquial_words:
                print word
    elif args.operation == "union":
        if args.type == "formal":
            for word in strong_formal_words.union(formal_seeds):
                print word
        elif args.type == "informal":
            for word in strong_colloquial_words.union(informal_seeds):
                print word
    elif args.operation == "diff":
        if args.type == "formal":
            for word in strong_formal_words.difference(formal_seeds):
                print word
        elif args.type == "informal":
            for word in strong_colloquial_words.difference(informal_seeds):
                print word
    if args.type == "neutral":
        for word in neutral_words:
            print word