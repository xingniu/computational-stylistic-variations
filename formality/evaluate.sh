#!/bin/bash

echo "Formality evaluation started at $(date)"

script_dir=`dirname $0`
. $script_dir/../global.cfg

## Data preparation
. $script_dir/prep-data.sh

## Experiment naming variables
if [[ $use_subspace == True ]]; then
	exp_dir=$exp_root_dir/$learning_method-$vsm_type-$subspace_train
else
	exp_dir=$exp_root_dir/$learning_method-$vsm_type
fi;
mkdir -p $exp_dir

## Train vector space models
. $root_dir/model/train-vsm.sh

## Calculate lexical formality
. $script_dir/calc-lexical-formality.sh

## Evaluation
echo " * Evaluating `basename $exp_dir` ..."
cd $root_dir

result=$exp_dir/evaluation
if [ ! -f $result ]; then
	echo "============= CTRW word pairs =============" > $result
	python -m formality.evaluate \
		-t ctrw           \
		-s $lexical_scores \
		-f $ctrw_word_pairs \
		>> $result
	echo "============== BEAN sentences =============" >> $result
	python -m formality.evaluate \
		-t bean                   \
		-s $lexical_scores         \
		-m $sentence_scoring        \
		-f $bean_sentence_scores     \
		-p $bean_tokenized_sentences  \
		>> $result
	echo "============== MASC sentences =============" >> $result
	python -m formality.evaluate \
		-t masc                   \
		-s $lexical_scores         \
		-m $sentence_scoring        \
		-f $masc_sentence_scores     \
		-p $masc_tokenized_sentences  \
		>> $result
	cat $result
fi;

echo "Formality evaluation finished at $(date)"