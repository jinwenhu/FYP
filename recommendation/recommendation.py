import os
import sys
from scipy import sparse
import numpy as np
import heapq
import json
from rand_walk import random_walk

### file names and paths
data_path = "../data"
crr_mtx_fname = "crr_mtx_1000_normalized"
moviefname = "movie_json_1000"

### parameters
alpha = 0.5
threshold = 1e-10
k = 10

### get ratings from standard input
ratings = []
rated_ids = []
for line in sys.stdin:
	movie_id, rating = map(int, line.split())
	ratings.append(rating)
	rated_ids.append(movie_id)

"""rated_ids = [1, 2, 3]
ratings = [1, 2, 3]"""

### load correlation matrix
dense_crr_mtx = np.loadtxt(os.path.join(data_path, crr_mtx_fname))
num_docs = len(dense_crr_mtx)
crr_mtx = sparse.csc_matrix(dense_crr_mtx)
    
### generate recommendations    
result_vec = random_walk(crr_mtx, num_docs, alpha, threshold, rated_ids, ratings)
    
topk_ids = heapq.nlargest(k, range(len(result_vec)), result_vec.__getitem__)

### output results
with open(os.path.join(data_path, moviefname)) as data_file:
    data = json.load(data_file)
    for id in topk_ids:
        temp_dict = data[id]
        movie_id = str(id)
        movie_name = temp_dict["name"]
        movie_description = temp_dict["description"]
        movie_image = temp_dict["url_image"]
        movie_url = temp_dict["url_web"]
        print '%s@%s@%s@%s@%s' % (movie_id, movie_name, movie_description, movie_image, movie_url)
