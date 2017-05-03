# Set up for "Get Started with NLP in Python"

This repo includes the notebooks, source data, and other materials for:
[Get Started with Natural Language Processing in Python](https://synecdoche.liber118.com/natural-language-processing-in-python-832b0a99791b).

## Virtual Environment
It's a good idea to use [virtualenv](https://virtualenv.pypa.io/) to
manage your Python 3 virtual environment:
```
virtualenv -p /usr/bin/python3 ~/venv
```

Then run:
```
source ~/venv/bin/activate
```

## Installation
To install the required Python libraries and related data sets:
```
pip install -r requirements.txt
python -m nltk.downloader punkt
python -m nltk.downloader wordnet
python -m textblob.download_corpora
python -m spacy download en
```

## TextBlob issues on Windows
The GitHub page for `textblob-aptagger` says the package is no longer needed as of TextBlob 0.11.0, 
which uses the NLTK perceptron tagger instead. Source code for `nltk.tag.perceptron` claims that 
it's a port of the TextBlob code. Not exactly -- however there may be issues on some versions of 
Windows.

If you run `pip install textblob` and DO NOT install `textblob-aptagger` that should work 
with minor changes to **Exercise 3** code and the `pynlp.py` module:

  * change `import textblob_aptagger as tag` to `import nltk`
  * change `tag.PerceptronTagger()` to `nltk.tag.PerceptronTagger()`
  * change `.tag(sent)` to `.tag(nltk.word_tokenize(sent))` (or the equivalent)
  
Results should look very much like the original results, although in general NTLK perceptron tagger 
has problems, e.g., it doesn't handle punctuation properly.
- kudos @blue_slacker

*NB: these course materials will shift from TextBlob to spaCy, soon, although the latter still 
has a few rough edges*

## Docker support (needs update)
A *Docker container* -- courtesy of @montyz, @ashapochka -- was
defined for an instance of this course a few months ago. May need
updates?

[https://github.com/montyz/nlp-12-14-2016](https://github.com/montyz/nlp-12-14-2016)
