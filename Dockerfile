FROM jupyter/minimal-notebook:latest

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader wordnet
RUN python -m textblob.download_corpora
RUN python -m spacy download en

# Launchbot labels
LABEL name.launchbot.io="Get Started with NLP in Python"
LABEL workdir.launchbot.io="/usr/workdir"
LABEL 8888.port.launchbot.io="Jupyter Notebook"

# Set the working directory
WORKDIR /usr/workdir

# Expose the notebook port
EXPOSE 8888

# Start the notebook server
CMD jupyter notebook --no-browser --port 8888 --ip=*
