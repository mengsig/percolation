
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from pylab import *
from matplotlib.widgets import Slider
from numba import njit

#first we create a function to create a grid
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
				data[counter] = np.random.uniform(0,1)
				counter+=1
				row[counter] = i
				col[counter] = i-1
				data[counter] = np.random.uniform(0,1)
				counter+=1
			if r > 0:
				row[counter] = i-N
				col[counter] = i
				data[counter] = np.random.uniform(0,1)
				counter+=1
				row[counter] = i
				col[counter] = i-N
				data[counter] = np.random.uniform(0,1)
				counter+=1

	return data, row, col
#calling the function as numba / jit compiler cant handle sparse arrays
def lattice(N):
	data, row, col = grid(N)
	nodes = int(N*N)
	GAdj = sp.sparse.coo_array((data, (row,col)), shape = (nodes,nodes))
	return sp.sparse.triu(GAdj, k=0)
_ = lattice(10)


#defining the reset function
def reset(event):
	alphaSlider.reset()
# pip install pillow
from PIL import Image

def display_percolation(field):
    return Image.fromarray(np.uint8((field) * 255))  # 0 ... 255

import time
N = 10000
nodes = N**2
alpha = 0.5
#creating using our lattice algorithm
t1 = time.time()
probMatrix = lattice(N)
print(f'Time taken to generate the latice and probability matrix using our algorithm: {time.time() - t1} seconds')
#creating the initial graph
updatedAdj = probMatrix > (1-alpha)
#now we find the largest component
noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
componentIndex = np.reshape(componentIndex, (N,N))
componentIndex = componentIndex % 2
ourImage = display_percolation(componentIndex)
ourImage.save(f'percolation_{N}_1.png')
ourImage.show()
