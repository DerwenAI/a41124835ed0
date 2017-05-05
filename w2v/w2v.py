#!/usr/bin/env python
# encoding: utf-8

import csv
import gensim
import logging
import sys

DEBUG = False # True


def load_sentences (term_path):
    global DEBUG
    sentences = []

    sent = []
    last_chap = None

    with open(term_path) as f:
        r = csv.reader(f, delimiter="\t")

        for term, chap, rank in r:
            rank = float(rank)

            if DEBUG:
                print("\t%s\t%s\t%0.4f" % (chap, term, rank))

            if chap != last_chap:
                if last_chap:
                    if DEBUG:
                        print(chap, sent)

                    sentences.append(sent)
                    sent = []

                last_chap = chap

            sent.append(term)

        # handle the dangling last element
        if DEBUG:
            print(chap, sent)

        sentences.append(sent)

    return sentences


def get_synset (model, query, topn=10):
    try:
        return sorted(model.most_similar(positive=[query], topn=topn), key=lambda x: x[1], reverse=True)
    except KeyError:
        return []


if __name__ == "__main__":
    MODEL_FILE = sys.argv[1]

    if len(sys.argv) > 2:
        # set up logging, train word2vec on the sentences
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # train a model, then save it
        term_path = sys.argv[2]
        sentences = load_sentences(term_path)

        model = gensim.models.Word2Vec(sentences, min_count=1)
        model.save(MODEL_FILE)

    else:
        # load a trained model
        model = gensim.models.Word2Vec.load(MODEL_FILE)

        # query the model through a REPL
        while True:
            try:
                query = input("\nquery? ")
                synset = get_synset(model, query, topn=10)
                print("most similar to", query, ":", synset)

            except KeyError:
                print("not found")
            except EOFError:
                print("\n")
                sys.exit(0)
