## Prepare BEAN sentences evaluation
## https://www.seas.upenn.edu/~epavlick/data.html
## - Sentence-level formality annotations for 4 genres (formality-corpus.tgz)
##   REF: Ellie Pavlick and Joel Tetreault. "An Empirical Analysis of Formality in Online Communication". TACL 2016.
##        Shibamouli Lahiri. "SQUINKY! A Corpus of Sentence-level Formality, Informativeness, and Implicature". arXiv:1506.02306

cd $exp_data_dir
if [ ! -f formality-corpus.tgz ]; then
	wget http://www.seas.upenn.edu/~nlp/resources/formality-corpus.tgz
	tar -xvf formality-corpus.tgz
fi;

bean_sentence_scores=$exp_data_dir/bean-sentence-scores
if [ ! -f $bean_sentence_scores ]; then
	echo " * Extracting BEAN sentence scores ..."
	for genre in answers email blog news; do
		cat $exp_data_dir/data-for-release/$genre \
			>> $bean_sentence_scores
	done;
fi;
bean_tokenized_sentences=$exp_data_dir/bean-tokenized-sentences
if [ ! -f $bean_tokenized_sentences ]; then
	echo " * Tokenizing BEAN sentences ..."
	iconv -f ISO-8859-2 -t UTF-8 \
		< $bean_sentence_scores   \
		| cut -f4 | sed "s/http[^ ]*//g"     \
		| sed "s/ n't/n't/g" | sed "s/ '/'/g" \
		| $moses_scripts_dir/tokenizer/normalize-punctuation.perl -l en  \
		| $moses_scripts_dir/tokenizer/tokenizer.perl -l en -a -no-escape \
		| perl -ne 'print lc' \
		>> $bean_tokenized_sentences
fi;
cd $root_dir