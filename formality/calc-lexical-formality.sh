cd $root_dir
lexical_scores=$exp_dir/lexical-scores
if [[ $learning_method == SVM ]]; then
	svm_model=$exp_dir/model
	if [ ! -f $svm_model- ]; then
		echo " * Training SVM for $vsm_corpus ..."
		python -m model.train-svm \
			-t $vsm_type      \
			-m $vsm_model      \
			-k $svm_kernel      \
			-p $formal_seeds     \
			-n $informal_seeds    \
			-c $vsm_components.npy \
			-s $svm_model
	fi;

	if [ ! -f $lexical_scores- ]; then
		echo " * Calculating lexical scores ..."
		python -m model.score-svm \
			-t $vsm_type \
			-m $vsm_model \
			-s $svm_model  \
			-d $debiasing   \
			-v $vocabulary   \
			-c $vsm_components.npy \
			> $lexical_scores
	fi;
elif [[ $learning_method == PCA ]]; then
	pca_model=$exp_dir/model
	if [ ! -f $pca_model.npy- ]; then
		echo " * Training PCA for $vsm_corpus ..."
		python -m model.train-pca \
			-k 1             \
			-t $vsm_type      \
			-m $vsm_model      \
			-p $formal_seeds    \
			-n $informal_seeds   \
			-s $similarity_metric \
			-i $vsm_components.npy \
			-c $pca_model
	fi;

	if [ ! -f $lexical_scores- ]; then
		echo " * Calculating lexical scores ..."
		python -m model.score-vec-sim \
			-t $vsm_type     \
			-m $vsm_model     \
			-d $debiasing      \
			-v $vocabulary      \
			-c $pca_model.npy    \
			-s $similarity_metric \
			-i $vsm_components.npy \
			> $lexical_scores
	fi;
elif [[ $learning_method == SimDiff ]]; then
	if [ ! -f $lexical_scores- ]; then
		echo " * Calculating lexical scores ..."
		python -m model.score-sim-diff \
			-t $vsm_type     \
			-m $vsm_model     \
			-v $vocabulary     \
			-p $formal_seeds    \
			-n $informal_seeds   \
			-s $similarity_metric \
			-c $vsm_components.npy \
			> $lexical_scores
	fi;
fi;