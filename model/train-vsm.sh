exp_vsm_dir=$exp_root_dir/vsm
mkdir -p $exp_vsm_dir

cd $root_dir
exp_vsm_corpus=$exp_vsm_dir/`basename $vsm_corpus`.lc.en
vsm_model=$exp_vsm_corpus.$vsm_type.$vsm_dimension
if [[ $vsm_type == lsa ]]; then
	similarity_metric=cosine
	svm_kernel=cosine
	if [ ! -f $exp_vsm_corpus.count ]; then
		echo " * Training an LSA for $vsm_corpus..."
		python $nlp_util/word-count.py \
			< $vsm_corpus.lc.en         \
			> $exp_vsm_corpus.count
	fi;
	if [ ! -f $vsm_model ]; then
		python -m model.train-lsa \
			-d $vsm_dimension      \
			-c $vsm_corpus.en       \
			-w $exp_vsm_corpus.count \
			-m $vsm_model
	fi;
elif [[ $vsm_type == w2v ]]; then
	similarity_metric=dot
	svm_kernel=linear
	if [ ! -f $vsm_model ]; then
		echo " * Training a Word2vec model for $vsm_corpus ..."
		$word2vec   \
			-cbow 0  \
			-iter 10  \
			-binary 1  \
			-threads 16 \
			-sample 1e-5 \
			-size $vsm_dimension    \
			-train $vsm_corpus.lc.en \
			-output $vsm_model
	fi;
fi;

if [[ $use_subspace == True ]]; then
	vsm_components=$vsm_model.$subspace_train.$subspace_dimension
	if [ ! -f $vsm_components.npy ]; then
		if [[ $subspace_train == seed ]]; then
			echo " * Generating a subspace using polar seeds ..."
			python -m model.train-pca \
				-t $vsm_type      \
				-m $vsm_model      \
				-p $formal_seeds    \
				-n $informal_seeds   \
				-s $similarity_metric \
				-k $subspace_dimension \
				-c $vsm_components
		elif [[ $subspace_train == ppdb ]]; then
			## Extract PPDB paraphrases
			. $root_dir/data-prep/prep-ppdb-phrase-pairs.sh
			
			echo " * Generating a subspace using PPDB paraphrases ..."
			python -m model.train-pca-pairs \
				-t $vsm_type        \
				-m $vsm_model        \
				-s $similarity_metric \
				-k $subspace_dimension \
				-p $ppdb_lexical_equivalents \
				-c $vsm_components
		fi;
	fi;
else
	vsm_components=/dev/null
fi;