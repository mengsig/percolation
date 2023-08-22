import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from pylab import *
from matplotlib.widgets import Slider

#defining the update function
def update(alpha):
	#first we rewire according to the alpha rule
	updatedAdj = probMatrix > (1-alpha)
	#now we find the largest component
	noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
	componentIndex = np.reshape(componentIndex, (N,N))
	ax.clear()
	ax.imshow(componentIndex) #change colormap here... i couldn't find a better one.

#defining the stop function
def reset(event):
	plt.pause(1)

#defining the resume function
def resume(event):
	plt.gcf().canvas.stop_event_loop()

#defining the number of nodes and grid size (N)
N = 1000
nodes = N**2
#defining the number of iterations in the time steps (resolution)
timeSteps = 250

#generating the graph just for the adjacency matrix
from networkx import grid_2d_graph, to_scipy_sparse_array, to_numpy_array
import time
t1 = time.time()
G = grid_2d_graph(N,N)
print(f'Time taken to generate networkx grid: {time.time() - t1} seconds')
#generating the sparse uniform probability matrix for checking if links get removed or not.
t1 = time.time()
GAdj = to_scipy_sparse_array(G, format = 'coo').astype(np.float32)
GAdj = sp.sparse.triu(GAdj, k=0)
#extract the values of the sparse array
dataOrig = GAdj.data
data = GAdj.data
#randomize the values of the sparse array and store them again
data = data * np.random.uniform(0,1, data.shape[0])
GAdj.data = data
#generate the sparse csr_array for fast comparisons and components computation 
probMatrix = sp.sparse.csr_array(GAdj)
print(f'Time taken to generate the probability matrix: {time.time() - t1} seconds')

#creating the initial graph
fig, ax = plt.subplots()
matplotlib.rcParams.update({'font.size':16})

#initializing the drawing
alpha = 0.5
update(alpha)

plt.subplots_adjust(bottom = 0.25)
axAlpha = plt.axes([0.25, 0.10, 0.65, 0.03])

#creating a slider.
alphaSlider = Slider(axAlpha, 'Probability', 0, 1.0)
alphaSlider.on_changed(update)

#creating the button (for stopping)
resetAlpha = plt.axes([0.025, 0.4, 0.10, 0.10])
button = Button(resetAlpha, 'Pause')
button.on_clicked(reset)
#creating the button (for resuming)
resetButton = plt.axes([0.025, 0.30, 0.10, 0.10])
startButton = Button(resetButton, 'Resume')
startButton.on_clicked(resume)

x = np.linspace(0,timeSteps, timeSteps)
#this line below is if you want non-linear time (ie. slow down as it gets to the critical point)
wait = 0.25*np.e**((-(x-timeSteps/2)**2)/(0.15**2*timeSteps**2))
#this line below is if you want linear time.
wait = 0.05*np.ones(timeSteps)
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

