import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from pylab import *
from matplotlib.widgets import Slider

#defining the update function
def update(alpha):
	data = dataInitial * np.random.uniform(0,1, dataInitial.shape[0])
	probMatrix.data = data
	updatedAdj = probMatrix > (1-alpha)
	noComponent, componentIndex = sp.sparse.csgraph.connected_components(updatedAdj, connection = 'weak', directed = False)
	componentIndex = np.reshape(componentIndex, (N,N))
	ax.clear()
	ax.imshow(componentIndex) #change colormap here... i couldn't find a better one.
#defining the reset function
def reset(event):
	alphaSlider.reset()

N = 250
nodes = N**2

#generating the graph just for the adjacency matrix
from networkx import grid_2d_graph, to_scipy_sparse_array, to_numpy_array
import time
t1 = time.time()
G = grid_2d_graph(N,N)
print(f'Time taken to generate networkx grid: {time.time() - t1} seconds')
#generating the sparse uniform probability matrix for checking if links get removed or not.
t1 = time.time()
probMatrix = to_scipy_sparse_array(G, format = 'coo')
probMatrix = sp.sparse.triu(probMatrix, k=0)
dataInitial = probMatrix.data
data = dataInitial * np.random.uniform(0,1, dataInitial.shape[0])
probMatrix.data = data

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

#creating a reset button for the critical value for the phase transition (alpha = 0.5)
resetAlpha = plt.axes([0.025, 0.5, 0.15, 0.15])
button = Button(resetAlpha, 'Reset to Critical Value')
button.on_clicked(reset)
plt.show()



