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

## Evaluation
| Method | VSM | Dimension | PCA-Data | Sub-Dim | CTRW Accuracy | BEAN Spearman's r | BEAN RMSE |
|--------|:---:|----------:|:--------:|--------:|:-------------:|:-----------------:|:---------:|
| SVM | W2V | 10 | | | 0.776 | 0.566 | 0.424 |
| PCA | W2V | 10 | | | 0.770 | 0.656 | 0.390 |
| SimDiff | W2V | 10 | | | 0.780 | 0.646 | 0.404 |
| SVM | W2V | 300 | ppdb | 20 | **0.844** | **0.662** | 0.372 |
| PCA | W2V | 300 | ppdb | 20 | 0.829 | **0.660** | 0.389 |
| SimDiff | W2V | 300 | ppdb | 20 | 0.832 | **0.662** | 0.386 |
| SVM | W2V | 300 | seed | 20 | 0.801 | 0.576 | 0.384 |
| PCA | W2V | 300 | seed | 20 | 0.768 | 0.653 | 0.377 |
| SimDiff | W2V | 300 | seed | 20 | 0.781 | 0.658 | 0.364 |
| SVM | LSA | 10 | | | 0.737 | **0.661** | 0.361 |
| PCA | LSA | 10 | | | 0.730 | 0.655 | **0.352** |
| SimDiff | LSA | 10 | | | 0.780 | 0.646 | **0.353** |
| SVM | LSA | 300 | ppdb | 20 | 0.712 | 0.457 | 0.641 |
| PCA | LSA | 300 | ppdb | 20 | 0.671 | 0.498 | 0.545 |
| SimDiff | LSA | 300 | ppdb | 20 | 0.686 | 0.492 | 0.563 |
| SVM | LSA | 300 | seed | 20 | 0.727 | 0.481 | 0.575 |
| PCA | LSA | 300 | seed | 20 | 0.699 | 0.522 | 0.513 |
| SimDiff | LSA | 300 | seed | 20 | 0.714 | 0.524 | 0.526 |

- VSM: Vector Space Model
- W2V: word2vec
- LSA: Latent Semantic Analysis
- CTRW: Choose the Right Word, see paper 2
- BEAN: Blog, Email, Answers and News, see paper 1
- RMSE: Root-Mean-Square Error