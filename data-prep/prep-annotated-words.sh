## Prepare style-annotated words
## http://www.cs.toronto.edu/~jbrooke/
## 1. formal/informal seed words (Formality_Word_Lists.zip)
##    REF: Julian Brooke, Tong Wang, and Graeme Hirst. "Automatic acquisition of lexical formality". COLING 2010.
## 2. 5-way annotations for 6 styles (style_annotations.zip)
##    REF: Julian Brooke and Graeme Hirst. "Hybrid models for lexical acquisition of correlated styles". IJCNLP 2013.
##         Julian Brooke and Graeme Hirst. "Supervised ranking of co-occurrence profiles for acquisition of continuous lexical attributes". COLING 2014.

cd $exp_data_dir
if [ ! -d Formality_Word_Lists ]; then
	wget http://www.cs.toronto.edu/~jbrooke/Formality_Word_Lists.zip
	unzip Formality_Word_Lists.zip -d Formality_Word_Lists -x *_seeds_100_CN.txt
fi;
if [ ! -f style_annotations.zip ]; then
	wget http://www.cs.toronto.edu/~jbrooke/style_annotations.zip
fi;

formal_seeds=$exp_data_dir/Formality_Word_Lists/formal_seeds_100.txt
informal_seeds=$exp_data_dir/Formality_Word_Lists/informal_seeds_100.txt
annotated_words=$exp_data_dir/annotated_words
formal_words=$exp_data_dir/formal_words
informal_words=$exp_data_dir/informal_words
neutral_words=$exp_data_dir/neutral_words
if [ ! -f $annotated_words ]; then
	for style in formal informal neutral; do
		style_words=$style\_words
		if [ ! -f ${!style_words} ]; then
			echo " * Extracting $style words ..."
			python $root_dir/data-prep/extract-annotated-words.py \
				-s $exp_data_dir/style_annotations.zip   \
				-f $exp_data_dir/Formality_Word_Lists.zip \
				-o union \
				-t $style \
				> ${!style_words}
			cat ${!style_words} >> $annotated_words
		fi;
	done;
fi;
cd $root_dir