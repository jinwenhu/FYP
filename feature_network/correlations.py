import numpy as np
from scipy.stats import pearsonr
from scipy.sparse import csr_matrix
import json
from scipy import sparse

def sparse_corrcoef(A, B=None):

    if B is not None:
        A = sparse.vstack((A, B), format='csr')

    A = A.astype(np.float64)

    # compute the covariance matrix
    # (see http://stackoverflow.com/questions/16062804/)
    A = A - A.mean(1)
    norm = A.shape[1] - 1.
    C = A.dot(A.T.conjugate()) / norm

    # the correlation coefficients are given by
    # C_{i,j} / sqrt(C_{i} * C_{j})
    d = np.diag(C)
    coeffs = C / np.sqrt(np.outer(d, d))

    return coeffs
movie_implicit_profiles = json.load(open("data/movie_implicit_tags"))
movie_explicit_profiles = json.load(open("data/movie_explicit_tags"))
movie_ids = map(int, movie_explicit_profiles.keys())
num_movies = len(movie_ids)
explicit_correlations = {}
implcit_correlation = {}

for movie_id in movie_ids:
	movie_explicit_profiles[str(movie_id)] = csr_matrix(movie_explicit_profiles[str(movie_id)])
	movie_implicit_profiles[str(movie_id)] = csr_matrix(movie_implicit_profiles[str(movie_id)])
for i in range(num_movies):
	if i % 1000 == 0:
		print i
	movie_id1 = movie_ids[i]
	explicit_correlations[movie_id1] = {}
	for j in range(i + 1, num_movies):
		movie_id2 = movie_ids[j]
		explicit_correlations[movie_id1][movie_id2] = sparse_corrcoef(movie_explicit_profiles[str(movie_id1)], movie_explicit_profiles[str(movie_id2)])
with open("data/movie_explicit_correlations") as f:
    json.dump(explicit_correlations, f)
del explicit_correlations

k = 0
for movie_id1 in movie_ids:
	if k % 1000 == 0:
		print k
	k += 1
	implicit_correlations[movie_id1] = {}
	for movie_id2 in movie_ids:
		if movie_id1 != movie_id2:
		    implicit_correlations[movie_id1][movie_id2] = sparse_corrcoef(movie_implicit_profiles[str(movie_id1)], movie_explicit_profiles[str(movie_id2)])
with open("data/movie_implicit_correlations") as f:
    json.dump(implicit_correlations, f)
