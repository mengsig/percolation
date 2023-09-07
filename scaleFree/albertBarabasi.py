import numpy as np
import scipy as sp
import networkx as nx
import matplotlib.pyplot as plt
from numba import njit, prange, jit
import time

@njit()
def barabasi_albert_edgelist(N, m):
	n = N - 3
	data = np.ones(N*m)
	row = np.zeros(N*m)
	col = np.zeros(N*m)
	#now we do the intiailization of the barabasi-albert model
	cumsum = np.zeros(N)
	counter = 0
	for i in range(m+1):
		for j in range(m):
			if i!=j:
				row[counter], col[counter] = i,j
				cumsum[i:m+1] += 1
				counter+=1
	if m == 1:
		cumsum[0] = 1
		cumsum[1] = 2
	else:
		cumsum[m] = 2*(m+1)
	#now we keep track of some things
	maxval = 2*m
	#now we start preferntially attaching
	for i in range(m, N):
		indices = []
		for links in range(m):
			prob = np.random.uniform(0,1)*maxval
			index = return_index(cumsum, prob, i)
			while index in indices:
				prob = np.random.uniform(0,1)*maxval
				index = return_index(cumsum, prob, i)
			indices.append(index)
			row[m*i+links] = i
			col[m*i+links] = index
			cumsum[index:i] += 1
			if links == 0:
				cumsum[i] = cumsum[i-1] + 1
			else:
				cumsum[i] += 2
			maxval = cumsum[i-1]
	return row, col, data

@njit()
def return_index(cumsum, prob, j):
	for i in range(j + 1):
		if cumsum[i] > prob:
			return i

#precompilation of jit code
_, __, ___ = barabasi_albert_edgelist(100, 1)
N = 10000
m = 2
p = 0.9
#t1 = time.time()
#GAdj = barabasi_albert(N,m)
#print(f'Time taken to generate a {N} node Albert-Barabasi network with kbar = {2*m} : {time.time() - t1} seconds')
t1 = time.time()
row, col, data = barabasi_albert_edgelist(N, m)
GAdj = sp.sparse.coo_array((data, (row, col)), shape = (N, N))
GAdj = GAdj + GAdj.T
print(f'Time taken to generate a {N} node Albert-Barabasi network with kbar = {2*m} : {time.time() - t1} seconds')
t1 = time.time()
G = nx.barabasi_albert_graph(N, m)
#GAdj = nx.to_scipy_sparse_array(G)
print(f'Networkx time to generate a {N} node Albert-Barabasi network with kbar = {2*m} : {time.time() - t1} seconds')
G = nx.from_scipy_sparse_array(GAdj)
#comment/uncomment here to unsee/see the barabasi albert graph
#fig = plt.figure(1)
#nx.draw(G, with_labels = True)
#here we show the degree distribution, ie. that it is truly scale free.
degree = GAdj.sum(axis=-1)
degreeNo, degreeCount = np.unique(degree, return_counts  = True)
degreeCount = degreeCount/degreeCount.max()
fig = plt.figure(2)
plt.loglog(degreeNo, degreeCount, '.')
plt.rcParams.update({'font.size' : 22})
plt.xlabel('degree', fontsize = 22)
plt.ylabel('probability', fontsize = 22)
plt.show()
