# Set up for "Get Started with NLP in Python"

This repo includes the notebooks, source data, and other materials for the course
[Get Started with Natural Language Processing in Python](https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b).

## Virtual Environment
It's recommended to use [virtualenv](https://virtualenv.pypa.io/) to
manage your Python 3 virtual environment:
```
virtualenv -p /usr/bin/python3 ~/venv
```

Then run:
```
source ~/venv/bin/activate
```

## Installation on a Laptop

To install the required Python libraries, Jupyter, and related data sets:
```
pip install -r requirements.txt

python -m nltk.downloader punkt
python -m nltk.downloader wordnet
python -m textblob.download_corpora
python -m spacy download en

pip install jupyter
pip install jupyterlab
```

## Start jupyter
```
jupyter notebook
```

## Installation on an Ubuntu server in a cloud

Alternatively, if you want install all of the required dependencies and run from an Ubuntu VM in the cloud, see the notes in [INSTALL.md](https://github.com/DerwenAI/a41124835ed0/blob/master/INSTALL.md)

## Command line test

To verify that the code in the `pynlp` library runs correctly, i.e., that the installation succeeded:
```
python pynlp.py html/article1.html a1.json
```
