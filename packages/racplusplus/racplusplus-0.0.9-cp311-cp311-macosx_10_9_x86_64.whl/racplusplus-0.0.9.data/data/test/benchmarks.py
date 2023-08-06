import sys
import os
# import pybind11
# Append the parent directory of racplusplus package to system path
# sys.path.append(os.path.join(os.path.abspath(__file__), "..", "..", "build"))
# sys.path.append("/Users/porterhunley/repos/racplusplus/build")
import numpy as np
import time
import racplusplus
import scipy as sp
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# print("\nSee how it performs with a connectivity matrix")

# Set up matrix by size and density

def run_test(rows, cols, seed):
    density =.1
    np.random.seed(42)

    num_ones = int(rows * cols * density)

    # Generate random indices for ones
    one_indices = np.random.choice(rows * cols, num_ones, replace=False)

    # Make sure both (i, j) and (j, i) indices exist
    rows_indices, cols_indices = np.unravel_index(one_indices, (rows, cols))
    all_indices = np.concatenate([rows_indices, cols_indices, cols_indices, rows_indices])
    all_indices = np.concatenate([all_indices, [rows-1]*rows, np.arange(rows)])

    all_cols = np.concatenate([cols_indices, rows_indices, rows_indices, cols_indices])

    # Include new cols indices for the connections from the last row to all other rows
    all_cols = np.concatenate([all_cols, np.arange(rows), [rows-1]*rows])

    # Create a boolean array for data
    data = np.ones(len(all_indices), dtype=bool)

    # Create the sparse symmetric matrix
    symmetric_connectivity_matrix = sp.sparse.csc_matrix((data, (all_indices, all_cols)), shape=(rows, cols))
    print("Done generating sparse unweighted connectivity matrix.\n")
    # pickle the matrix
    # with open('connectivity_matrix.pkl', 'wb') as f:
    #     pickle.dump(symmetric_connectivity_matrix, f)

    # print(symmetric_connectivity_matrix.todense()[17,6])

    # Load the matrix
    # with open('connectivity_matrix.pkl', 'rb') as f:
    #     symmetric_connectivity_matrix = pickle.load(f)

    # symmetric_connectivity_matrix = sp.sparse.csc_matrix((10, 10))

    max_merge_distance = .24
    batch_size = 1000
    no_processors = 8
    test_matrix = np.random.random((rows, 768))

    print("Running RAC from Python using numpy data matrix and scipy sparse csc connectivity matrix.")
    # yep.start('rac.prof')
    start = time.time()
    labels = racplusplus.rac(test_matrix, max_merge_distance, symmetric_connectivity_matrix, "symmetric", batch_size, no_processors)
    end = time.time()
    print(f"Time to run RAC: {end - start}")
    # yep.stop()
    print(f"Point Cluster Assignments: {len(set(labels))}")

    # start = time.time()
    clustering = AgglomerativeClustering(
        n_clusters=None, 
        linkage='average',
        distance_threshold=max_merge_distance, 
        # connectivity=symmetric_connectivity_matrix,
        metric='cosine').fit(test_matrix)
    
    print(f"Sklearn Point Cluster Assignments: {len(set(clustering.labels_))}")

    # print(f"Sklearn Point Cluster Assignments: {len(set(clustering.labels_))}")
    # end = time.time()
    # print(f"Time to run sklearn: {end - start}")

    # # rac_labels = labels
    # # sklearn_labels = clustering.labels_

    # # sklearn_label_map = {key:i for (i, key) in enumerate(sklearn_labels)}
    # # rac_label_map = {key:i for (i, key) in enumerate(rac_labels)}
    # # transformed_sklearn = [sklearn_label_map[i] for i in sklearn_labels]
    # # trans_rac_labels = [rac_label_map[i] for i in rac_labels]

    # print(f"Sklearn: {transformed_sklearn}")
    print(f"RAC--->: {labels}")

    # return trans_rac_labels == transformed_sklearn


# result = True
# seed = 82
# try:
#     while result:
#         print(f"Running test on seed {seed}")
#         result = run_test(10, 10, seed)
#         # if (seed == 29):
#         #     result = True
#         seed += 1
# except:
#     print(f"Test failed on seed {seed-1}.")
# print(f"Test failed on seed {seed-1}.")


# while True:
print(run_test(100, 100, 42))
# print(run_test(20, 20, 83))
