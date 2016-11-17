import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import bz2
from gensim import corpora, models, similarities
from heapq import nlargest
from operator import itemgetter

data_path = r'../data'
wn_corpus_name = 'wn_tfidf.mm'
wn_model_name = 'wn.tfidf_model'
wn_index_name = 'wn_sp_sim.index'
wn_iddict_name = 'wn_idwords.dict'
wiki_corpus_name = 'wiki_en_tfidf.mm'
wn_model_name = 'wiki_en.tfidf_model'
wiki_index_name = 'wiki_sp_sim.index'
wiki_iddict_name = 'wiki_en_wordids.txt.bz2'
threshold = 0.5
kwlist = ['alien', 'battle']

def update_act_value(old_dict, new_dict):
    for key in new_dict:
        if key in old_dict:
            old_dict[key] += new_dict[key]
        else:
            old_dict[key] = new_dict[key] 

def get_sp_index(index_fname, corpus, id_dict):
    if os.path.isfile(index_fname):
        print("loading index %s" % index_fname)
        index = similarities.SparseMatrixSimilarity.load(index_fname)
    else:
        print("creating index %s" % index_fname)
        #tfidf = models.TfidfModel(corpus)
        index =  similarities.SparseMatrixSimilarity(corpus, num_features=len(list(id_dict)))
        index.save(index_fname)
    return index     

def gen_new_features(kwlist, corpuslist, tfidf_models, index_list, iddict_list, threshold, k): # get top k features
    
    # get similarities bettwen keywords and cus
    print("getting new features")
    num_corpus = len(corpuslist)
    cu_dicts = [{}, {}]
    kw_act_dict = {}
    
    #cu_bow_lists = [list(corpus) for corpus in corpuslist]

    print("computing similarities between clues and cus")
    
    for i in range(num_corpus):
        id_dict = iddict_list[i]
        cu_dict = cu_dicts[i]
        corpus = corpuslist[i]
        dictionary = iddict_list[i]
        tfidf = tfidf_models[i]
        index = index_list[i]
        #index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(list(id_dict)))
        
        for kw in kwlist:
            kw_bow_vec = dictionary.doc2bow(kw.lower().split())
            kw_tfidf_vec = tfidf[kw_bow_vec]
            sims = index[kw_tfidf_vec]
            sims_dict = dict(list(enumerate(sims)))
            update_act_value(cu_dict, sims_dict)
    
    # filter out cus under the threshold
    print("spreading the activation vals from cus to new features")
    
    for i in range(num_corpus):
        cu_dict = cu_dicts[i]
        corpus = corpuslist[i]
        id_dict = iddict_list[i]
        for doc_no in cu_dict:
            clue_doc_sim = cu_dict[doc_no]
            if clue_doc_sim >= threshold:
                doc = dict(corpus[doc_no])
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

if __name__ == '__main__':
    wn_corpus = corpora.MmCorpus(os.path.join(data_path, wn_corpus_name))
    wn_iddict = corpora.Dictionary.load(os.path.join(data_path, wn_iddict_name))
    wn_index = get_sp_index(os.path.join(data_path, wn_index_name), wn_corpus, wn_iddict)
    wn_model = models.TfidfModel.load(os.path.join(data_path,"wn.tfidf_model"))
    
    wiki_corpus = corpora.MmCorpus(os.path.join(data_path, wiki_corpus_name))
    wiki_iddict = corpora.Dictionary.load_from_text(bz2.BZ2File(os.path.join(data_path, wiki_iddict_name)))
    wiki_index =  get_sp_index(os.path.join(data_path, wiki_index_name), wiki_corpus, wiki_iddict)
    wiki_model = models.TfidfModel.load(os.path.join(data_path,"wiki_en.tfidf_model"))
    
    topk_dict = gen_new_features(kwlist, [wn_corpus, wiki_corpus], [wn_model, wiki_model], [wn_index, wiki_index], [wn_iddict, wiki_iddict], threshold, 10)
    print(topk_dict)
