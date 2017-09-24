## Extract PPDB paraphrases
## http://paraphrase.org/#/download
## - S-size lexical paraphrases (ppdb-2.0-s-lexical.gz)
##   REF: Ellie Pavlick, Pushpendre Rastogi, Juri Ganitkevich, Ben Van Durme, and Chris Callison-Burch. "PPDB 2.0: Better paraphrase ranking, fine-grained entailment relations, word embeddings, and style classification". ACL 2015.

cd $exp_data_dir
ppdb_lexical_equivalents=$exp_data_dir/ppdb-lexical-equivalents
if [ ! -f $ppdb_lexical_equivalents ]; then
	wget http://nlpgrid.seas.upenn.edu/PPDB/eng/ppdb-2.0-s-lexical.gz
	gzip -dc ppdb-2.0-s-lexical.gz        \
		| python $nlp_util/PPDB-extract.py \
			-e Equivalence                  \
		> $ppdb_lexical_equivalents
fi;
cd $root_dir