"""import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)"""

import os
import bz2
from gensim import corpora, models, similarities
from heapq import nlargest
from operator import itemgetter

data_path = r'../data'
wn_model_name = 'wn_tfidf.mm'
wn_iddict_name = 'wn_idwords.dict'
wiki_model_name = 'wiki_en_tfidf.mm'
wiki_iddict_name = 'wiki_en_wordids.txt.bz2'
threshold = 0.3
kwlist = ['alien']

def update_act_value(old_dict, new_dict):
    for key in new_dict:
        if key in old_dict:
            old_dict[key] += new_dict[key]
        else:
            old_dict[key] = new_dict[key]       

def gen_new_features(kwlist, corpuslist, iddict_list, k): # get top k features
    # get similarities bettwen keywords and cus
    print("getting new features")
    num_corpus = len(corpuslist)
    cu_dicts = [{}, {}]
    kw_act_dict = {}
    cu_bow_lists = [list(corpus) for corpus in corpuslist]

    print("computing similarities between clues and cus")
    for kw in kwlist:
        for i in range(num_corpus):
            id_dict = iddict_list[i]
            cu_dict = cu_dicts[i]
            corpus = corpuslist[i]
            dictionary = iddict_list[0]
            tfidf = models.TfidfModel(corpus)
            kw_vec = dictionary.doc2bow([kw])
            index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(list(id_dict)))
            sims = index[kw_vec]
            sims_dict = dict(list(enumerate(sims)))
            update_act_value(cu_dict, sims_dict)
    
    # filter out cus under the threshold
    print("spreading the activation vals from cus to new features")
    for i in range(num_corpus):
        cu_dict = cu_dicts[i]
        cu_bow_list = cu_bow_lists[i]
        id_dict = iddict_list[i]
        for doc_no in cu_dict:
            clue_doc_sim = cu_dict[doc_no]
            if clue_doc_sim >= threshold:
                doc = dict(cu_bow_list[doc_no])
                new_kw_act_dict = {}
                for kwid in doc:
                    kw = id_dict.get(kwid)
                    new_kw_act_dict[kw] = clue_doc_sim * doc[kwid]
                    update_act_value(kw_act_dict, new_kw_act_dict)
    
    print("getting topk features")
    new_features = {}
    for kw, score in nlargest(k, kw_act_dict.items(), key=itemgetter(1)):
        new_features[kw] = score
    return new_features

wn_corpus = corpora.MmCorpus(os.path.join(data_path, wn_model_name))
wn_iddict = corpora.Dictionary.load(os.path.join(data_path, wn_iddict_name))
wiki_corpus = corpora.MmCorpus(os.path.join(data_path, wiki_model_name))
wiki_iddict = corpora.Dictionary.load_from_text(bz2.BZ2File(os.path.join(data_path, wiki_iddict_name)))
topk_dict = gen_new_features(kwlist, [wn_corpus, wiki_corpus], [wn_iddict, wiki_iddict], 10)
print(topk_dict)
