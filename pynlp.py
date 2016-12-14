#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
from collections import defaultdict
from collections import namedtuple
import json
import math
import re
import sys
import textblob
import textblob_aptagger as tag
import unicodedata


PAT_PUNCT = re.compile(r'^\W+$')
PAT_SPACE = re.compile(r'\_+$')
TAGGER = tag.PerceptronTagger()

WordNode = namedtuple('WordNode', 'raw, root, pos')


def extract_html (file):
  with open(file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

    for div in soup.find_all("div", id="article-body"):
      for p in div.find_all("p"):
        yield p.get_text()


def cleanup_text (text):
  x = " ".join(map(lambda x: x.strip(), text.split("\n"))).strip()
  unicodedata.normalize('NFKD', x).encode('ascii','ignore')
  x = x.replace('“', '"').replace('”', '"')
  x = x.replace("‘", "'").replace("’", "'")
  x = x.replace('…', '...').replace('–', '-')

  return x


def is_not_word (word):
  global PAT_PUNCT, PAT_SPACE
  return PAT_PUNCT.match(word) or PAT_SPACE.match(word)


def load_stopwords (file):
  stopwords = set([])

  with open(file, "r") as f:
    for line in f.readlines():
      stopwords.add(line.strip().lower())

  return stopwords



def annotate (sent):
  global TAGGER
  ts = TAGGER.tag(sent)

  for raw, pos in ts:
    pos_kind = pos[0].lower()
    w = textblob.Word(raw.lower())
    root = str(w)

    if is_not_word(raw[0]) or (pos == "SYM"):
      pos = "."
    elif pos_kind in ["n", "v"]:
      root = w.lemmatize(pos_kind)

    yield WordNode(raw=raw, pos=pos, root=root)


def parse_html (file):
  for text in extract_html(file):
    for sent in textblob.TextBlob(cleanup_text(text)).sentences:
      yield [lex for lex in annotate(str(sent))]



def pretty_print (obj, indent=False):
  if indent:
    return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
  else:
    return json.dumps(obj, sort_keys=True)


def full_parse (html_file, json_file):
  with open(json_file, "w") as f:
    for sent_lex in parse_html(html_file):
      f.write(pretty_print(sent_lex))
      f.write("\n")


def lex_iter (json_file):
  with open(json_file, "r") as f:
    for line in f.readlines():
      for lex in list(map(WordNode._make, json.loads(line))):
        yield lex


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: ./pynlp.py <HTML file>")
    sys.exit(-1)

  file = sys.argv[1]
  print(file)

  for text in extract_html(file):
    clean = cleanup_text(text)
    print(clean)

    for sent in textblob.TextBlob(clean).sentences:
      print(">", sent)

      for lex in annotate(str(sent)):
        print(lex)
