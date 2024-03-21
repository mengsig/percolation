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

#from numba import prange
#@njit(parallel = True)
#def generate_colors(componentIndex, counts):
#    newColors = np.zeros(componentIndex.shape)
#    randCols = np.random.uniform(0,1,counts.shape[0])
#    for i in prange(componentIndex.shape[0]):
#        if counts[componentIndex[i]] < 10:
#            newColors[i] = 0
#        else:
#            newColors[i] = randCols[componentIndex[i]]#counts[componentIndex[i]]
#    return newColors

from numba import prange
@njit(parallel = True)
def generate_colors(componentIndex, counts, N):
    newColors = np.zeros((N,N,3))
    randCols = np.random.uniform(0,1,(counts.shape[0],3))
    for i in prange(N):
        for j in range(N):
            if counts[componentIndex[i, j]] <= 1:
                newColors[i, j, :] = np.ones(3)
            else:
                newColors[i, j, :] = randCols[componentIndex[i, j]]#counts[componentIndex[i]]
    return newColors
#defining the update function
def update(alpha):
	#first we rewire according to the alpha rule
    updatedAdj = probMatrix > (1-alpha)
	#now we find the largest component

    noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
    vals, counts = np.unique(componentIndex, return_counts = True)
    componentIndex = np.reshape(componentIndex, (N,N))
    newColors = generate_colors(componentIndex, counts, N)
    #componentIndex = componentIndex % 100
    #newColors = newColors*componentIndex
    newColorsMax = newColors.max()
    center = int(N/2)
    size1 = int(center/3)
    size2 = int(size1/3)
    size3 = int(size2/3)
    ax[0,0].clear()
    ax[0,0].imshow(newColors) #change colormap here... i couldn't find a better one.
    ax[0,1].clear()
    ax[0,1].imshow(newColors[center-size1:center+size1, center-size1:center+size1])
    ax[1,0].clear()
    ax[1,0].imshow(newColors[center-size2:center+size2, center-size2:center+size2])
    ax[1,1].clear()
    ax[1,1].imshow(newColors[center-size3:center+size3, center-size3:center+size3])

#defining the reset function
def reset(event):
	alphaSlider.reset()

import time
N = int(1024)
nodes = N**2

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

import os, datetime;
datestring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
print (datestring);
os.mkdir(datestring);

fig.savefig(f'{datestring}/percolation{N}.pdf')
plt.show()

#creating 4 new figs
updatedAdj = probMatrix > (1-alpha)
#now we find the largest component
noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
vals, counts = np.unique(componentIndex, return_counts = True)
componentIndex = np.reshape(componentIndex, (N,N))
newColors = generate_colors(componentIndex, counts, N)
#componentIndex = componentIndex % 100
#newColors = newColors*componentIndex
newColorsMax = newColors.max()
center = int(N/2)
size1 = int(center/3)
size2 = int(size1/3)
size3 = int(size2/3)

fig1 = plt.figure()
plt.imshow(newColors)
fig1.savefig(f'{datestring}/percolation{N}_0.pdf')
fig2 = plt.figure()
plt.imshow(newColors[center-size1:center+size1, center-size1:center+size1])
fig2.savefig(f'{datestring}/percolation{N}_1.pdf')
fig3 = plt.figure()
plt.imshow(newColors[center-size2:center+size2, center-size2:center+size2])
fig3.savefig(f'{datestring}/percolation{N}_2.pdf')
fig4 = plt.figure()
plt.imshow(newColors[center-size3:center+size3, center-size3:center+size3])
fig4.savefig(f'{datestring}/percolation{N}_3.pdf')


