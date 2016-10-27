# this file processes wordnet synsets and output save it as a gensim tfidf corpus

#############################
# get all synsets from wordnet
import json
from nltk.corpus import wordnet as wn
fname = "../data/synsets.json"
syn_list = []
for synset in wn.all_synsets():
    syn_dict = {}
    syn_dict["lemmas"] = synset.lemma_names()
    syn_dict["definition"] = synset.definition()
    syn_dict["examples"] = synset.examples()
    syn_list.append(syn_dict)
with open(fname, 'w') as f:
    json.dump(syn_list, f)

#####################
# create tfidf corpus
from gensim import corpora, models
import logging
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# treat all lemmas in a synset as a doc
texts = [syn["lemmas"] for syn in syn_list]

# save word2id dictionary
dictionary = corpora.Dictionary(texts)
dictionary.save('../data/wn_idwords.dict')
corpus_bow = [dictionary.doc2bow(text) for text in texts]

#save tfidf corpus
tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]
corpora.MmCorpus.serialize('../data/wn_tfidf.mm', corpus_bow)
