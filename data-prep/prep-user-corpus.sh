## Preprocess user corpus: tokenization and lowercasing

if [[ $input_file == "" ]]; then
	input_file=$1
	. `dirname $0`/../my_global.cfg
fi;

if [[ $prep_file == "" ]]; then
	prep_file=$1.tok.lc
fi;

if [ ! -f $prep_file ]; then
	echo " * Preprocessing $input_file ..."
	cat $input_file        \
		| $moses_scripts_dir/tokenizer/normalize-punctuation.perl -l en  \
		| $moses_scripts_dir/tokenizer/tokenizer.perl -l en -a -no-escape \
		| perl -ne 'print lc' \
		> $prep_file
fi;