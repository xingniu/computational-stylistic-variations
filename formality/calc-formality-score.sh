#!/bin/bash

while getopts ":i:o:slph" opt; do
	case $opt in
	s)
		sort=True ;;
	l)
		lex=True ;;
	p)
		prep=True ;;
	i)
		input_file=$OPTARG ;;
	o)
		output_file=$OPTARG ;;
	h)
		echo "Usage: calc-formality-score.sh -i FILE -o FILE [-s] [-l] [-p]"
		echo "-i input file (absolute path)"
		echo "-o output file (absolute path)"
		echo "-s sort lines by formality score"
		echo "-l only output lexical scores"
		echo "-p preprocess input file (tokenization and lowercasing)"
		exit 0 ;;
    \?)
		echo "Invalid option: -$OPTARG" >&2
		exit 1 ;;
    :)
		echo "Option -$OPTARG requires an argument." >&2
		exit 1 ;;
	esac
done

echo "Calculating formality scores started at $(date)"

script_dir=`dirname $0`
. $script_dir/../global.cfg

## Experiment naming variables
exp_data_dir=$exp_root_dir/data
mkdir -p $exp_data_dir
exp_dir=$(mktemp -d)
echo "temporary files are stored in $exp_dir"

## Prepare style-annotated words
. $root_dir/data-prep/prep-annotated-words.sh

## Preprocess "ICWSM 2009 Spinn3r Blog Dataset"
. $root_dir/data-prep/prep-spinn3r.sh

if [[ $prep == True ]]; then
	prep_file=$exp_dir/input.tok.lc
	. $script_dir/../data-prep/prep-user-corpus.sh
	input_file=$prep_file
fi;

echo " * Collecting the vocabulary ..."
vocabulary=$exp_dir/vocabulary
cat $input_file  \
	| tr -d '\15' \
	| tr ' ' '\n'  \
	| sort | uniq   \
	> $vocabulary

## Train vector space models
. $root_dir/model/train-vsm.sh

## Calculate lexical formality
. $script_dir/calc-lexical-formality.sh

scored_file=$exp_dir/scored-file
if [[ $lex == True ]]; then
	mv $lexical_scores $scored_file
else
	echo " * Calculating score per line ..."
	cd $root_dir
	python -m formality.calc-formality-score \
		-i $input_file     \
		-s $lexical_scores  \
		-m $sentence_scoring \
		> $scored_file
fi;

if [[ $sort == True ]]; then
	echo " * Sorting ..."
	if [[ $lex == True ]]; then
		sort -k2 -n $scored_file > $output_file
	else
		sort -k1 -n $scored_file > $output_file
	fi;
else
	mv $scored_file $output_file
fi;

rm -r $exp_dir
echo "Calculating formality scores finished at $(date)"