import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.widgets import Slider
import networkx as nx
########## Here we do some introductory stuff with percolation ###########
#update function
def update(val):
	GW = G.copy()
	for i,j in GW.edges():
		if np.random.uniform(0,1) > val:
			GW.remove_edge(i,j)
	wcc = [GW.subgraph(c).copy() for c in nx.connected_components(GW)]
	ax.clear()
	for index, sg in enumerate(wcc):
		color = (np.random.uniform(0,1), np.random.uniform(0,1),np.random.uniform(0,1))
		nx.draw(sg, pos, ax, edge_color = color, node_color = color) 
	fig.canvas.draw_idle()
N = 500 #size of the grid

# Creating the subplot

#Generating the grid
G = nx.grid_2d_graph(N,N)
#Generating the position to be a square.
pos = dict((N,N) for N in G.nodes())

#creating the initial graph
fig, ax = plt.subplots()

# initializing the graph
nx.draw(G, pos, ax) 

plt.subplots_adjust(bottom = 0.25)
#creating the buttons
axAlpha = plt.axes([0.25, 0.10, 0.65, 0.03])
alphaSlider = Slider(axAlpha, 'Probability', 0, 1.0)
alphaSlider.on_changed(update)
plt.show()

