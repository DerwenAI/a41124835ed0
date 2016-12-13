#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
from collections import namedtuple
import textblob
import json
import re
import sys
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


def json_iter (path):
  with open(path, "r") as f:
    for line in f.readlines():
      yield json.loads(line)


def pretty_print (obj, indent=False):
  if indent:
    return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
  else:
    return json.dumps(obj, sort_keys=True)


def parse_html (file):
  for text in extract_html(file):
    for sent in textblob.TextBlob(cleanup_text(text)).sentences:
      yield [lex for lex in annotate(str(sent))]


def full_parse (html_file, json_file):
  with open(json_file, "w") as f:
    for sent_lex in parse_html(html_file):
      f.write(pretty_print(sent_lex))
      f.write("\n")


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
