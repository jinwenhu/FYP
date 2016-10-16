import json
from nltk.corpus import wordnet as wn
fname = "synsets.json"
syn_list = []
for synset in wn.all_synsets():
    syn_dict = {}
    syn_dict["lemmas"] = synset.lemma_names()
    syn_dict["definition"] = synset.definition()
    syn_dict["examples"] = synset.examples()
    syn_list.append(syn_dict)
with open(fname, 'w') as f:
    json.dump(syn_list, f)

from gensim import corpora, models, similarities
from collections import Counter
import logging
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

texts = [syn["lemmas"] for syn in syn_list]

dictionary = corpora.Dictionary(texts)
dictionary.save('wn_kwid.dict')
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
with open("wn_bow", "w") as f:
    f.write(str(list(corpus_tfidf)))

