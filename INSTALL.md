## Install Jupyter on Ubuntu 16.04 LTS

```
sudo bash
apt-get update

apt-get install virtualenv python-pip
apt-get install python-dev python3-dev libevent-dev
apt-get install ipython ipython-notebook

pushd /usr/bin/
rm -r python
ln -s python3 python

rm -f /etc/boto.cfg
exit

virtualenv -p /usr/bin/python3 ~/venv
source ~/venv/bin/activate
```


## Install Course Dependencies

```
git clone https://github.com/DerwenAI/a41124835ed0.git

pip install -r requirements.txt
python -m nltk.downloader punkt
python -m nltk.downloader wordnet
python -m textblob.download_corpora
python -m spacy download en

pip install jupyter
pip install jupyterlab
```

## Launch Jupyter

```
source ~/venv/bin/activate
cd a41124835ed0

jupyter-notebook --no-browser --port=8888 --NotebookApp.token='' --ip='0.0.0.0' &
```

Then use your server's IP address in the following format:

```
http://<ip_addr>:8888/
```
