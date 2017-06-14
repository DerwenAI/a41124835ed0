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

## Docker support

A *Docker container* -- courtesy of @montyz, @ashapochka -- was
defined for an instance of this course a few months ago:
[https://github.com/montyz/nlp-12-14-2016](https://github.com/montyz/nlp-12-14-2016)

That's been extended by @odewahn to run on [Launchbot](https://launchbot.io) 
and [JupyterHub](https://jupyterhub.readthedocs.io/en/latest/)

## Command line test

To exercise the code in the `pynlp` library:
```
python pynlp.py html/article1.html a1.json
```
