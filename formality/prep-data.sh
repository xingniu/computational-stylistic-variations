#!/bin/bash

## Experiment naming variables
exp_data_dir=$exp_root_dir/data
mkdir -p $exp_data_dir

## Prepare style-annotated words
. $root_dir/data-prep/prep-annotated-words.sh

## Prepare MASC sentences evaluation
. $root_dir/data-prep/prep-masc-sentences.sh

## Prepare BEAN sentences evaluation
. $root_dir/data-prep/prep-bean-sentences.sh

## Prepare CTRW evaluation
. $root_dir/data-prep/prep-ctrw-word-pairs.sh

## Prepare the vocabulary
vocabulary=$exp_data_dir/vocabulary
if [ ! -f $vocabulary ]; then
	echo " * Collecting the vocabulary ..."
	cat $annotated_words        \
		$ctrw_word_pairs         \
		$bean_tokenized_sentences \
	    $masc_tokenized_sentences  \
		| tr -d '\15' | tr ' ' '\n' \
		| sort | uniq                \
		> $vocabulary
fi;

sentence_words=$exp_data_dir/sentence_words
if [ ! -f $sentence_words ]; then
	echo " * Collecting words in sentences ..."
	cat $bean_tokenized_sentences \
	    $masc_tokenized_sentences  \
		| tr -d '\15' | tr ' ' '\n' \
		| sort | uniq                \
		> $sentence_words
fi;

if [[ $mono_corpus == spinn3r ]]; then
	## Preprocess "ICWSM 2009 Spinn3r Blog Dataset"
	. $root_dir/data-prep/prep-spinn3r.sh
elif [[ $mono_corpus == user ]]; then
	## Preprocess/link user-provided corpus
	vsm_corpus=$exp_data_dir/$(echo `basename $user_corpus` | cut -d. -f1)
	if [[ $user_corpus_prep == yes ]]; then
		input_file=$user_corpus
		prep_file=$vsm_corpus.lc.en
		. $root_dir/data-prep/prep-user-corpus.sh
	else
		ln -sf $user_corpus $vsm_corpus.lc.en
	fi;
fi;