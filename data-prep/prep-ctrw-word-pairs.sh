## Prepare CTRW evaluation
## http://www.cs.toronto.edu/~jbrooke/
## - Choose the Right Word (CTRW) synonym pairs (Formality_Word_Lists.zip)
##   REF: Julian Brooke, Tong Wang, and Graeme Hirst. "Automatic acquisition of lexical formality". COLING 2010.

ctrw_word_pairs=$exp_data_dir/ctrw-word-pairs
if [ ! -f $ctrw_word_pairs ]; then
	echo " * Extracting CTRW word pairs ..."
	cat $exp_data_dir/Formality_Word_Lists/CTRWpairsfull.txt \
		| tr '/' ' ' \
		> $ctrw_word_pairs
	echo "" >> $ctrw_word_pairs
fi;