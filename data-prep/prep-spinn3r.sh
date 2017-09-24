## Preprocess "ICWSM 2009 Spinn3r Blog Dataset"
## http://www.icwsm.org/data/

vsm_corpus=$exp_data_dir/$(echo `basename $spinn3r` | cut -d. -f1)
if [ ! -f $vsm_corpus.en ]; then
	echo " * Extracting Spinn3r text ..."
	python $nlp_util/Spinn3r-2009-extract.py \
		-f $spinn3r                           \
		-l en -e title description -u -c       \
		| sed "s/[\xe2\x80\x99]/'/g"            \
		| sed "s/[\xe2\x80\xa6]/.../g"           \
		| sed 's/[\xe2\x80\x9c\xe2\x80\x9d]/"/g'  \
		| sed "s/^---[0-9a-zA-Z~-]\{11\}---$/---/" \
		| $moses_scripts_dir/ems/support/split-sentences.perl -l en    \
		| sed "s/^<P>$//g"                           \
		| $moses_scripts_dir/tokenizer/normalize-punctuation.perl -l en  \
		| $moses_scripts_dir/tokenizer/tokenizer.perl -l en -a -no-escape \
		> $vsm_corpus.en
fi;
if [ ! -f $vsm_corpus.lc.en ]; then
	echo " * Lowercasing Spinn3r ..."
	cat $vsm_corpus.en  \
		| sed '/^$\|^---$/d' \
		| perl -ne 'print lc' \
		> $vsm_corpus.lc.en
fi;