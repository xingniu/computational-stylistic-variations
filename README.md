# computational-stylistic-variations
Stylistic Variations in Distributional Vector Space Models

This repository contains implementations for
1. Xing Niu, Marianna Martindale, and Marine Carpuat. "A Study of Style in Machine Translation: Controlling the Formality of Machine Translation Output". EMNLP 2017.
2. Xing Niu and Marine Carpuat. "Discovering Stylistic Variations in Distributional Vector Space Models via Lexical Paraphrases". Workshop on Stylistic Variation at EMNLP 2017.

## Dependencies
- Python 2.7
- [gensim](https://radimrehurek.com/gensim/)
- [scikit-learn](http://scikit-learn.org)
- Other toolkits and data (see [global.cfg](global.cfg))

## Usage Instructions
1. Set up parameters and pointers in [global.cfg](global.cfg).
2. Initialize and test.
```bash
> bash formality/evaluate.sh
```
3. Calculate lexical formality for lines of text.
```bash
> bash formality/calc-formality-score.sh -i input-file -o output-file -s
```
```
Usage: calc-formality-score.sh -i INPUT_FILE -o OUTPUT_FILE [-s]
Optional arguments:
  -i INPUT_FILE    input file (absolute path)
  -o OUTPUT_FILE   output file (absolute path)
  -s               sort lines by formality score
```

## Results
| Method | VSM | Dimension | PCA-Data | Sub-Dim | CTRW Accuracy | BEAN Spearman's r |
|--------|:---:|----------:|:--------:|--------:|:-------------:|:-----------------:|
| SVM | W2V | 10 | | | 0.776 | 0.566 |
| PCA | W2V | 10 | | | 0.770 | 0.656 |
| SimDiff | W2V | 10 | | | 0.780 | 0.646 |
| SVM | W2V | 300 | ppdb | 20 | **0.844** | **0.662** |
| PCA | W2V | 300 | ppdb | 20 | 0.829 | **0.660** |
| SimDiff | W2V | 300 | ppdb | 20 | 0.832 | **0.662** |
| SVM | W2V | 300 | seed | 20 | 0.801 | 0.576 |
| PCA | W2V | 300 | seed | 20 | 0.768 | 0.653 |
| SimDiff | W2V | 300 | seed | 20 | 0.781 | 0.658 |
| SVM | LSA | 10 | | | 0.737 | **0.661** |
| PCA | LSA | 10 | | | 0.730 | 0.655 |
| SimDiff | LSA | 10 | | | 0.780 | 0.646 |
| SVM | LSA | 300 | ppdb | 20 | 0.712 | 0.457 |
| PCA | LSA | 300 | ppdb | 20 | 0.671 | 0.498 |
| SimDiff | LSA | 300 | ppdb | 20 | 0.686 | 0.492 |
| SVM | LSA | 300 | seed | 20 | 0.727 | 0.481 |
| PCA | LSA | 300 | seed | 20 | 0.699 | 0.522 |
| SimDiff | LSA | 300 | seed | 20 | 0.714 | 0.524 |

- VSM: Vector Space Model
- W2V: word2vec
- LSA: Latent Semantic Analysis
- CTRW Accuracy: Choose the Right Word, see paper 2
- BEAN Spearman's r: blog, email, answers and news, see paper 1