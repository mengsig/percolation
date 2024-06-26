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
	length = 2*nodes - 2*N
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
				#row[counter] = i
				#col[counter] = i-1
				#data[counter] = np.random.uniform(0,1)
				#counter+=1
			if r > 0:
				row[counter] = i-N
				col[counter] = i
				data[counter] = np.random.uniform(0,1)
				counter+=1
			#	row[counter] = i
			#	col[counter] = i-N
			#	data[counter] = np.random.uniform(0,1)
			#	counter+=1

	return data, row, col
#calling the function as numba / jit compiler cant handle sparse arrays
def lattice(N):
	data, row, col = grid(N)
	nodes = int(N*N)
	GAdj = sp.sparse.coo_array((data, (row,col)), shape = (nodes,nodes))
	return sp.sparse.triu(GAdj, k=0)
_ = lattice(10)


#defining the update function
def update(alpha):
	#first we rewire according to the alpha rule
    updatedAdj = probMatrix > (1-alpha)
	#now we find the largest component

    noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
    componentIndex = np.reshape(componentIndex, (N,N))
    componentIndex = componentIndex % 12
    center = int(N/2)
    size1 = int(center/3)
    size2 = int(size1/3)
    size3 = int(size2/3)
    print(componentIndex[center-size1:center+size1,center-size1:center+size1].shape)
    ax[0,0].clear()
    ax[0,0].imshow(componentIndex, cmap = 'Paired') #change colormap here... i couldn't find a better one.
    ax[0,1].clear()
    ax[0,1].imshow(componentIndex[center-size1:center+size1, center-size1:center+size1], cmap = 'Paired')
    ax[1,0].clear()
    ax[1,0].imshow(componentIndex[center-size2:center+size2, center-size2:center+size2], cmap = 'Paired')
    ax[1,1].clear()
    ax[1,1].imshow(componentIndex[center-size3:center+size3, center-size3:center+size3], cmap = 'Paired')

#defining the reset function
def reset(event):
	alphaSlider.reset()

import time
N = int(3*2700)
nodes = N**2

#generating the graph just for the adjacency matrix
#t1 = time.time()
#from networkx import grid_2d_graph, to_scipy_sparse_array, to_numpy_array
#t1 = time.time()
#G = grid_2d_graph(N,N)
##generating the sparse uniform probability matrix for checking if links get removed or not.
#GAdj = to_scipy_sparse_array(G, format = 'coo').astype(np.float32)
#GAdj = sp.sparse.triu(GAdj, k=0)
##extract the values of the sparse array
#data = GAdj.data
##randomize the values of the sparse array and store them again
#data = data * np.random.uniform(0,1, data.shape[0])
#GAdj.data = data
##generate the sparse csr_array for fast comparisons and components computation 
#probMatrix = sp.sparse.csr_array(GAdj)
#print(f'Time taken to generate the lattice and probability matrix using networkx and numpy: {time.time() - t1} seconds')
#creating using our lattice algorithm
t1 = time.time()
probMatrix = lattice(N)
print(f'Time taken to generate the latice and probability matrix using our algorithm: {time.time() - t1} seconds')
#creating the initial graph
fig, ax = plt.subplots(2,2, figsize = (24,18))
matplotlib.rcParams.update({'font.size':16})

#initializing the drawing
alpha = 0.5
update(alpha)

plt.subplots_adjust(bottom = 0.25)
axAlpha = plt.axes([0.25, 0.10, 0.65, 0.03])

#creating a slider.
alphaSlider = Slider(axAlpha, 'Probability', 0.2, 0.8)
alphaSlider.on_changed(update)

#creating a reset button for the critical value for the phase transition (alpha = 0.5)
resetAlpha = plt.axes([0.025, 0.1, 0.10, 0.10])
button = Button(resetAlpha, 'Reset to Critical Value')
button.on_clicked(reset)
plt.show()

