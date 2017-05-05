# Word2Vec example

Build the model:
```
./w2v.py model.dat terms.tsv
```

Query the model:
```
./w2v.py model.dat
```

The data file `terms.tsv` has 10K elements from a much larger file,
with the keyphrases from 843 unique "documents" represented.
Realistically, you want many more "documents" in a Word2Vec model
before its results begin to make sense.

This is enough to show how to call the functions from `gensim`.
