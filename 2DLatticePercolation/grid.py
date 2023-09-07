import numpy as np
import scipy as sp
import networkx as nx
from numba import njit, prange
import matplotlib.pyplot as plt

def make_matrix(N):
	nodes = int(N*N)
	M = np.zeros((nodes,nodes))
	for r in range(N):
		for c in range(N):
			i = r*N + c
			if c > 0:
				M[i-1,i] = 1
				M[i, i-1] = 1
			if r > 0:
				M[i-N, i] = 1
				M[i, i-N] = 1
	return M

@njit()
def grid(N):
	nodes = int(N*N)
	length = 4*nodes - 4*N
	data = np.zeros(length)
	row = np.zeros(length)
	col = np.zeros(length)
	counter = 0
	for r in range(N):
		for c in range(N):
			i = r*N + c
			if c > 0:
				row[counter] = i-1
				col[counter] = i
				data[counter] = 1
				counter+=1
				row[counter] = i
				col[counter] = i-1
				data[counter] = 1
				counter+=1
			if r > 0:
				row[counter] = i-N
				col[counter] = i
				data[counter] = 1
				counter+=1
				row[counter] = i
				col[counter] = i-N
				data[counter] = 1
				counter+=1

	return data, row, col

def lattice(N):
	data, row, col = grid(N)
	return sp.sparse.coo_array((data, (row,col)), shape = (nodes,nodes))

N = 250
nodes = int(N*N)
grid(2)
import time
t1 = time.time()
GAdjCoo = lattice(N)
print(time.time() - t1)
t1 = time.time()
GAdj = make_matrix(N)
print(time.time() - t1)
t1 = time.time()
G = nx.grid_2d_graph(N,N)
GAdj1 = nx.to_scipy_sparse_array(G)
print(time.time() - t1)
print(GAdj)
print(GAdj1)
print((GAdj == GAdj1).sum())
print((GAdj == GAdjArray).sum())
