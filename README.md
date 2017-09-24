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