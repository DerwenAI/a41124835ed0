#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
from collections import namedtuple
import json
import spacy
import sys
import unicodedata

SPACY_NLP = None
WordNode = namedtuple('WordNode', 'raw, root, pos')


def load_stopwords (stop_file):
    """
    load the stopwords list
    """
    stopwords = set([])

    with open(stop_file) as f:
        for line in f.readlines():
            stopwords.add(line.strip().lower())

    return stopwords


def extract_html (html_file):
    """
    use BeautifulSoup4 to extract the text from an HTML file
    """
    with open(html_file) as f:
        soup = BeautifulSoup(f, "html.parser")

        for div in soup.find_all("div", id="article-body"):
            for p in div.find_all("p"):
                yield p.get_text()


def cleanup_text (text):
    """
    clean up (normalize) the unicode in a raw text
    """
    x = " ".join(map(lambda x: x.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("`` ", '"').replace("''", '"')
    x = x.replace('…', '...').replace('–', '-')
    x = x.replace("\\u00a0", " ").replace("\\u2014", " - ").replace("\\u2022", "*")
    x = x.replace("\\u2019", "'").replace("\\u201c", '"').replace("\\u201d", '"')

    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8')

    return x


def annotate (doc, span, debug=False):
    """
    annotate each token in a sentence
    """
    for i in range(span.start, span.end):
        token = doc[i]

        if debug:
            print(token.text, token.tag_, token.pos_, token.lemma_)

        if token.pos_[0] in ["N", "V"]:
            root = token.lemma_
        else:
            root = token.text.lower()

        if token.pos_ in ["HYPH", "PUNCT"]:
            pos = "."
        else:
            pos = token.tag_

        yield WordNode(raw=token.text, root=root, pos=pos)


def parse_html (html_file, debug=False):
    """
    parse an HTML file, sentence by sentence
    """
    global SPACY_NLP

    if not SPACY_NLP:
        SPACY_NLP = spacy.load("en")

    for text in extract_html(html_file):
        doc = SPACY_NLP(cleanup_text(text))

        for span in doc.sents:
            yield [lex for lex in annotate(doc, span, debug)]


def pretty_print (obj, indent=False):
    """
    pretty print JSON objects
    """
    if indent:
        return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
    else:
        return json.dumps(obj, sort_keys=True)


def full_parse (html_file, json_file):
    """
    parse an HTML file, saving the annotated results as a JSON file
    """
    with open(json_file, "w") as f:
        for sent_lex in parse_html(html_file):
            f.write(pretty_print(sent_lex))
            f.write("\n")


def lex_iter (json_file):
    """
    iterate through the parsed results in a JSON file
    """
    with open(json_file) as f:
        for line in f.readlines():
            for lex in list(map(WordNode._make, json.loads(line))):
                yield lex


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./pynlp.py <HTML_file> <JSON_file")
        sys.exit(-1)

    html_file = sys.argv[1]
    json_file = sys.argv[2]

    for sent in parse_html(html_file, debug=True):
        print(sent)
        print("---")

    full_parse(html_file, json_file)

    for lex in lex_iter(json_file):
        print(lex)
