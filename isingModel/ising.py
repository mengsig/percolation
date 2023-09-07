############# This is the ising model simulation ####################

#first we import the necessary modules
import numpy as np
import matplotlib.pyplot as plt 
import scipy as sp
from pylab import * 
from matplotlib.widgets import Slider
from numba import njit, prange
import time


#first we create a function to create a lattice
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


#here we create a precompiled function for returning either a 1 for positive and -1 for negative.
@njit()
def binary(val):
	if val < 0:
		return -1
	else:
		return 1

#here we create a precompiled and multiprocessing function that initalizes the random state of the grid
@njit(parallel = True)
def psi_initialization(N):
	states = np.random.uniform(-1,1, N) #create an array of uniformly distributed values between -1, 1
	for i in prange(N):
		states[i] = binary(states[i]) #check if the input of this array is positive or negative, and return 1 or -1 respectively. 
	return states

#here we create another precompiled and multiprocessing function that updates the value of Psi.
@njit(parallel = True)
def psi_update(Psi, probVec, T = 2):
	newVec = Psi*probVec #this vector is the input vector times Psi. Probvec = GAdj @ Psi.
	for i in prange(Psi.shape[0]): #iterate in parallel 
		if newVec[i] > 0:
			pass
		else:
			if np.random.uniform(0,1) < np.e**(newVec[i]/T): #check to see the random flip passes the probability given the (potential) energy differencas a function of temperature.
				Psi[i] = Psi[i]*-1 #if yes... make it negative
	return Psi

#calling the function as numba / jit compiler cant handle sparse arrays
def lattice(N):
	data, row, col = grid(N)
	nodes = int(N*N)
	GAdj = sp.sparse.coo_array((data, (row,col)), shape = (nodes,nodes))
	return GAdj

#creating our update function for the figure and processing the evolution of the process
def update(GAdj, Psi, T, stepcount = 1):
	#first we rewire according to the alpha rule
	for i in range(stepcount):
		probVec = GAdj@Psi #figure out the sum of states of your neighbor
		Psi = psi_update(Psi, probVec, T) 
	#now we find the largest component
	PsiColor = np.reshape(Psi, (N,N))
	ax.clear()
	ax.imshow(PsiColor) #change colormap here... i couldn't find a better one.

#defining the stop function
def reset(event):
	plt.pause(1)

#defining the resume function
def resume(event):
	plt.gcf().canvas.stop_event_loop()

#precompiling the functions for small values (super cheap)
_ = lattice(10)
_ = psi_initialization(10)


############## Here begins the tuneable parameters #################
N = 1000 #grid size (nodes = NxN)
nodes = int(N*N)
T = 1.5 #temperature
stepcount = 2 #how frequently you want to plot the state.

#creating our lattice
GAdj = lattice(N)
GAdj = sp.sparse.csr_array(GAdj) #converting it to csr as that is super efficient for algorthmic processes
Psi = psi_initialization(nodes)

#initializing the drawing
fig, ax = plt.subplots(figsize=(15,15))
matplotlib.rcParams.update({'font.size':16})

#creating the button (for stopping)
resetAlpha = plt.axes([0.0, 0.4, 0.10, 0.10])
button = Button(resetAlpha, 'Pause')
button.on_clicked(reset)
#creating the button (for resuming)
resetButton = plt.axes([0.0, 0.30, 0.10, 0.10])
startButton = Button(resetButton, 'Resume')
startButton.on_clicked(resume)

#creating an infinite while looop to draw the plot
k=0
while k < 1:
	if plt.fignum_exists(1): #simply check if the figure exists, otherwise, break the infinite while loop.
		update(GAdj, Psi, T, stepcount)
		plt.show(block = False)
		plt.pause(0.00001) #just to make a dynamic figure --- it makes the plt.show "stop" immediately after each k -> allows redrawing.
	else:
		break

