## Prepare MASC sentences evaluation
## https://www.seas.upenn.edu/~epavlick/data.html
## - Human scores of formality for words, phrases, and sentences (style-scores.tar.gz)
##   REF: Ellie Pavlick and Ani Nenkova. "Inducing Lexical Style Properties for Paraphrase and Genre Differentiation". NAACL 2015.

cd $exp_data_dir
if [ ! -f style-scores.tar.gz ]; then
	wget http://www.seas.upenn.edu/~nlp/resources/style-scores.tar.gz
	tar -xvf style-scores.tar.gz naacl-2015-style-scores/formality/human/sentence-scores
fi;

masc_sentence_scores=$exp_data_dir/naacl-2015-style-scores/formality/human/sentence-scores
masc_tokenized_sentences=$exp_data_dir/masc-tokenized-sentences
if [ ! -f $masc_tokenized_sentences ]; then
	echo " * Tokenizing MASC sentences ..."
	cut -f3 $exp_data_dir/naacl-2015-style-scores/formality/human/sentence-scores \
	    | sed "s/http[^ ]*//g" | sed "s/ n't/n't/g" | sed "s/ '/'/g"    \
		| $moses_scripts_dir/tokenizer/normalize-punctuation.perl -l en  \
		| $moses_scripts_dir/tokenizer/tokenizer.perl -l en -a -no-escape \
		> $masc_tokenized_sentences
fi;
cd $root_dir