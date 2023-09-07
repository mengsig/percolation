import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from pylab import *
from matplotlib.widgets import Slider
from numba import prange, njit, jit


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
				data[counter] = np.random.uniform()
				counter+=1
				row[counter] = i
				col[counter] = i-1
				data[counter] = np.random.uniform()
				counter+=1
			if r > 0:
				row[counter] = i-N
				col[counter] = i
				data[counter] = np.random.uniform()
				counter+=1
				row[counter] = i
				col[counter] = i-N
				data[counter] = np.random.uniform()
				counter+=1

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
	ax.clear()
	ax.imshow(componentIndex) #change colormap here... i couldn't find a better one.
	#here we start plotting the distriubtion of component sizes
	import time
	t1 = time.time()
	unique, counts = np.unique(componentIndex, return_counts = True)
	t1 = time.time()
	plotData = generate_histogram_data(componentIndex, counts)
	newUnique, newCounts = np.unique(plotData, return_counts = True)
	for i in range(newCounts.shape[0]):
		newCounts[i] = newCounts[i]/newUnique[i]
	newCounts = newCounts/newCounts.sum()
	#creating the net plot bx
	bx.clear()
	#comment the two lines below if you don't want to lock the axis.
	bx.set_xlim(0.5, 2*nodes)
	bx.set_ylim(0.5/nodes, 2)
	bx.set_xlabel('Cluster Size, L', fontsize = 22)
	bx.set_ylabel('probability, p', fontsize = 22)
	bx.loglog(newUnique, newCounts, 'kx')

#defining the data extraction function for bx.
@njit(parallel = True)
def generate_histogram_data(componentIndex, counts):
	dataStruct = np.zeros(componentIndex.shape)
	for i in prange(componentIndex.shape[0]):
		for j in range(componentIndex.shape[0]):
			dataStruct[i,j] = counts[componentIndex[i,j]]
	return dataStruct
		
#defining the stop function
def reset(event):
	plt.pause(1000)

#defining the resume function
def resume(event):
	plt.gcf().canvas.stop_event_loop()

#defining the number of nodes and grid size (N)
N = 500
nodes = N**2
#defining the number of iterations in the time steps (resolution)
timeSteps = 250

#generating the graph just for the adjacency matrix
############ UNCOMMENT BELOW IF YOU WANT TO COMPARE COMPUTATIONAL EFFICIENCY OF THE GENERATED ALGORITHM TO CREATE THE GRID ##########

#generating the graph just for the adjacency matrix
#from networkx import grid_2d_graph, to_scipy_sparse_array, to_numpy_array
#t1 = time.time()
#G = grid_2d_graph(N,N)
#print(f'Time taken to generate networkx grid: {time.time() - t1} seconds')
##generating the sparse uniform probability matrix for checking if links get removed or not.
#t1 = time.time()
#GAdj = to_scipy_sparse_array(G, format = 'coo').astype(np.float32)
#GAdj = sp.sparse.triu(GAdj, k=0)
#print(GAdj.shape)
##extract the values of the sparse array
#dataOrig = GAdj.data
#data = GAdj.data
##randomize the values of the sparse array and store them again
#data = data * np.random.uniform(0,1, data.shape[0])
#GAdj.data = data
##generate the sparse csr_array for fast comparisons and components computation 
#probMatrix = sp.sparse.csr_array(GAdj)
#print(probMatrix.shape)
#print(f'Time taken to generate the probability matrix: {time.time() - t1} seconds')
t1 = time.time()
probMatrix = lattice(N)
GAdj = probMatrix > 0
dataOrig = GAdj.data
print(probMatrix.shape)
print(f'New algorithm time to create the probability matrix from scratch - including the grid itself: {time.time() - t1} seconds')

#creating the initial graph
fig, (ax, bx) =  plt.subplots(1,2)
matplotlib.rcParams.update({'font.size':22})
plt.rcParams.update({'font.size' : 22})
bx.set_xlabel('Cluster Size, L')
bx.set_ylabel('Probability, p')

#initializing the drawing
alpha = 0.5
update(alpha)

plt.subplots_adjust(bottom = 0.25)
axAlpha = plt.axes([0.25, 0.10, 0.65, 0.03])

#creating a slider.
alphaSlider = Slider(axAlpha, 'Probability', 0, 1.0)
alphaSlider.on_changed(update)

#creating the button (for stopping)
resetAlpha = plt.axes([0.00, 0.4, 0.10, 0.10])
button = Button(resetAlpha, 'Pause')
button.on_clicked(reset)
#creating the button (for resuming)
resetButton = plt.axes([0.00, 0.30, 0.10, 0.10])
startButton = Button(resetButton, 'Resume')
startButton.on_clicked(resume)

x = np.linspace(0,timeSteps, timeSteps)
#this line below is if you want non-linear time (ie. slow down as it gets to the critical point)
wait = 0.25*np.e**((-(x-timeSteps/2)**2)/(0.15**2*timeSteps**2))
#this line below is if you want linear time.
wait = 0.001*np.ones(timeSteps)
counter = 0
while counter < timeSteps:
	if counter == 0:
		probMatrix.data = dataOrig*np.random.uniform(0,1,dataOrig.shape[0])
	ax.clear()
	alphaSlider.set_val(counter/timeSteps)
	plt.show(block = False)
	plt.pause(wait[counter])
	counter +=1
	if counter >= timeSteps - 1:
		probMatrix.data = dataOrig*np.random.uniform(0,1,dataOrig.shape[0])
		while counter >= 1:
			ax.clear()
			alphaSlider.set_val(counter/timeSteps)
			plt.show(block = False)
			plt.pause(wait[counter])
			counter += -1
plt.show()

