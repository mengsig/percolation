import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.widgets import Slider
import networkx as nx
########## Here we do some introductory stuff with percolation ###########

### First we define our update function
def update(val): 
	GW = G.copy() #copy our graph so we dont change it
	for i,j in GW.edges(): #loop through all edges in our graph
		k = i[0] + N*i[1] #simply change indices from (1,1) ->> 26
		l = j[0] + N*j[1]
		if probMatrix[k][l] > val: #use the prob matrix for conditional
			GW.remove_edge(i,j)
	wcc = [GW.subgraph(c).copy() for c in sorted(nx.connected_components(GW), key = len, reverse = True)] #here we simply create subgraphs for coloring
	ax.clear()
	for index, sg in enumerate(wcc): #enumerate through the subgraphs to draw them according to color.
		color = allColors[index] 
		nx.draw(sg, pos, ax, edge_color = color, node_color = color) 
	fig.canvas.draw_idle()

def reset(event):
	alphaSlider.reset()

N = 20 #size of the grid
allColors = np.random.uniform(0,1,(N*N,3))
# Creating the subplot

#Generating the grid
G = nx.grid_2d_graph(N,N)
GAdj = nx.to_numpy_array(G)
probMatrix = GAdj * np.random.uniform(0,1,GAdj.shape)

#creating the position
pos = dict((N,N) for N in G.nodes())

#creating the initial graph
fig, ax = plt.subplots()
matplotlib.rcParams.update({'font.size':16})
#initializing the drawing
nx.draw(G, pos, ax) 

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

