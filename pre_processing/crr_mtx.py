import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import bz2
import math
import json
import numpy as np
from gensim import corpora, models, similarities
from heapq import nlargest
from operator import itemgetter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import spreading

data_path = r'../data'
moviefname = "movie_json_1000"
crr_mtx_fname = "crr_mtx_1000"

wn_corpus_name = 'wn_tfidf.mm'
wn_model_name = 'wn.tfidf_model'
wn_index_name = 'wn_sp_sim.index'
wn_iddict_name = 'wn_idwords.dict'
wiki_corpus_name = 'wiki_en_tfidf.mm'
wn_model_name = 'wiki_en.tfidf_model'
wiki_index_name = 'wiki_sp_sim.index'
wiki_iddict_name = 'wiki_en_wordids.txt.bz2'
threshold = 0.5

def read_data(fname, data_path):
    with open(os.path.join(data_path, moviefname)) as data_file:
        data = json.load(data_file)
    doc_data = [" ".join((movie["keyword"], movie["description"])) for movie in data]
    return doc_data

def read_kwlist(fname, data_path):
    with open(os.path.join(data_path, moviefname)) as data_file:
        data = json.load(data_file)
    kw_data = [movie["keyword"].split() for movie in data]
    return kw_data


def BM25(features, doc_freq_list, doc_len, defualt_idf, avgdl, docs_idf):
    features_feq_mtx = np.array(count_vectorizer.transform(features).todense())
    freq_feature_in_doc = []
    idf_list = []
    for feature_doc in features_feq_mtx:
        i = 0
        while feature_doc[i] == 0:
              i += 1
              if i >= len(doc_freq_list):
                  break
        if i >= len(doc_freq_list):
            freq_feature_in_doc.append(0)
            idf_list.append(defualt_idf)
        else: 
            freq_feature_in_doc.append(doc_freq_list[i])
            idf_list.append(docs_idf[i])
    result_list= [freq_feature_in_doc[i] * 3 * idf_list[i]/ \
        (freq_feature_in_doc[i] + 0.5 + 1.5 * doc_len / avgdl) for i in range(len(features))]
    return sum(result_list)
    
if __name__ == "__main__":
    doc_data = read_data(moviefname, data_path) # list of strings
    kw_data = read_kwlist(moviefname, data_path)
    num_docs = len(doc_data)
    default_idf = math.log(num_docs, math.e)
    
    count_vectorizer = CountVectorizer(stop_words='english')
    freq_term_matrix = count_vectorizer.fit_transform(doc_data)
    freq_term_matrix_dense = np.array(freq_term_matrix.todense())
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(freq_term_matrix)
    docs_idfs = tfidf.idf_
    doc_len_list = [sum(doc_freq_list) for doc_freq_list in freq_term_matrix_dense]
    avgdl = sum(doc_len_list) / num_docs

    wn_corpus = corpora.MmCorpus(os.path.join(data_path, wn_corpus_name))
    wn_iddict = corpora.Dictionary.load(os.path.join(data_path, wn_iddict_name))
    wn_index = spreading.get_sp_index(os.path.join(data_path, wn_index_name), wn_corpus, wn_iddict)
    wn_model = models.TfidfModel.load(os.path.join(data_path,"wn.tfidf_model"))
    wiki_corpus = corpora.MmCorpus(os.path.join(data_path, wiki_corpus_name))
    wiki_iddict = corpora.Dictionary.load_from_text(bz2.BZ2File(os.path.join(data_path, wiki_iddict_name)))
    wiki_index =  spreading.get_sp_index(os.path.join(data_path, wiki_index_name), wiki_corpus, wiki_iddict)
    wiki_model = models.TfidfModel.load(os.path.join(data_path,"wiki_en.tfidf_model"))

    crr_mtx = np.zeros((num_docs, num_docs))
    for i in range(num_docs):
        print(i)
        features = spreading.gen_new_features(kw_data[i], [wn_corpus, wiki_corpus], [wn_model, wiki_model], [wn_index, wiki_index], [wn_iddict, wiki_iddict], threshold, 6).keys()
        crr_mtx[i] = [BM25(features, freq_term_matrix_dense[j], doc_len_list[j], default_idf, avgdl, docs_idfs) for j in range(num_docs)] 
    
    np.savetxt(os.path.join(data_path, crr_mtx_fname), crr_mtx)
