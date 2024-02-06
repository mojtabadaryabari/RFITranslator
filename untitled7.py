# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 09:53:38 2023

@author: mojta
"""

import os
import json
import re
import matplotlib.pyplot as plt

import numpy as np


from sklearn.cluster import DBSCAN

Data=[]


dirList = os.listdir("./") # current directory


# Define a regular expression pattern to capture the text between */ and /*
pattern = r'/\*(.*?)\*/'

# Use re.findall to find all matches of the pattern in the text

input_file = "./Test/test.txt"



with open(input_file, 'r') as file:
    code_content = file.read()

# Use re.findall to find all matches of the pattern in the text
matches = re.findall(pattern, code_content)


s = ''.join(str(x) for x in matches)   


my_list = json.loads(s)

# Select the first element (index 0) from the list


Data.append(my_list)


input_file = "./Test/test1.txt"

with open(input_file, 'r') as file:
    code_content = file.read()

# Use re.findall to find all matches of the pattern in the text
matches = re.findall(pattern, code_content)


s = ''.join(str(x) for x in matches)   
my_list = json.loads(s)

Data.append(my_list)




dim1_size = len(Data)
dim2_size = max(len(level) for level in Data)
dim3_size = max(len(sublist) for level in Data for sublist in level)
dim4_size = max(len(subsublist) if isinstance(subsublist, list) else 1
               for level in Data
               for sublist in level
               for subsublist in sublist)

# Create a NumPy array with the determined sizes
originalarray = np.zeros((dim1_size, dim2_size, dim3_size, dim4_size), dtype=int)

# Fill the array with your data
for i, level in enumerate(Data):
    for j, sublist in enumerate(level):
        for k, subsublist in enumerate(sublist):
            if isinstance(subsublist, list):
                originalarray[i, j, k, :len(subsublist)] = subsublist
            else:
                originalarray[i, j, k, 0] = subsublist

# Create a NumPy array with the determined sizes


# Get the shape of the original array
original_shape = originalarray.shape

# Reshape the array to 2D by flattening the last two dimensions
new_shape = (original_shape[0] , original_shape[2] * original_shape[3]* original_shape[1])
X = originalarray.reshape(new_shape)



def custom_metric(z, y):
    # x, y are two vectors
    # distance(.,.) calculates count of elements when both xi and yi are True
    size=len(z);
    same=0;
    for i in range(0, size-1):
        if (z[i]==y[i]):
            same=same+1;
    return pow(size-same,2);


db = DBSCAN(min_samples=1, metric=custom_metric, eps=5, p=1).fit(X)


labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)


unique_labels = set(labels)
core_samples_mask = np.zeros_like(labels, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True


colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = labels == k

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=14,
    )

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=4,
    )




plt.title(f"Estimated number of clusters: {n_clusters_}")
plt.show()
representative_points = []

for label in unique_labels:
    if label == -1:  # Noise points have label -1
        continue

    cluster_points = X[labels == label]
    representative_points.append(X[labels == label])

# Printing representative points
for i, point in enumerate(representative_points):
    print(f"Cluster {i + 1} Representative Point: {point[0]}")

