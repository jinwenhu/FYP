import numpy as np
import os
from scipy import sparse
data_path = "../data"
crr_mtx_fname = "crr_mtx_1000"
dense_crr_mtx = np.loadtxt(os.path.join(data_path, crr_mtx_fname))
num_docs = len(dense_crr_mtx)

#dense_crr_mtx = sparse.rand(num_docs, num_docs, density=0.01, format='csc', dtype=float, random_state=None).toarray()

crr_mtx_t = dense_crr_mtx
for i in range(num_docs):
    crr_mtx_t[i][i] = 0
    col_sum = crr_mtx_t[i].sum()
    if col_sum != 0:
        crr_mtx_t[i] = crr_mtx_t[i] / col_sum
    else: crr_mtx_t[i] = np.ones((1, num_docs)) / num_docs
dense_crr_mtx = crr_mtx_t.transpose()
np.savetxt(os.path.join(data_path, "crr_mtx_1000_normalized"), dense_crr_mtx)
#np.savetxt(os.path.join(data_path, "crr_mtx_1000_rand"), dense_crr_mtx)
