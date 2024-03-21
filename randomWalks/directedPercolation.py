import numpy as np
from numba import njit, prange
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#first we initialize our lattice
@njit()
def lattice(N):
    ourLattice = np.zeros((N,int(2*N)))
    ourLattice[::, -1] = np.random.uniform(0,1,N)
    ourLattice[::, -1] = ourLattice[::,-1] > 0.5
    return ourLattice 
#find zero entry
@njit()
def find_zero(lattice):
    degree = lattice.sum(axis=0)
    for k in range(degree.shape[0]):
        if degree[k] > 0:
            return k
    else:
        return 0
#now we define directed percolation time step
@njit(parallel = True)
def directedUpdate(lattice, p = 0.50):
    #first we find the row we should enter.
    t = find_zero(lattice)
    ourN = lattice.shape[0]
    if t == 0:
        length = lattice.shape[-1]
        lattice[::, int(length/2):length] = lattice[::, 0:int(length/2)]
        lattice[::, 0:int(length/2)] = 0
    ourArray = lattice[::, t]
    for k in prange(ourN):
        if k == 0:
            tempSum = ourArray[k:k+3] #[k:k+2]
            tempSum[-1] = ourArray[-1] #creating reflective boundaries
        elif k == ourN - 1:
            tempSum = ourArray[k-2:k+1] #[k-1:k+1]
            tempSum[0] = ourArray[0] #creating reflective ounbdaries
        else:
            tempSum = ourArray[k-1:k+2]
        ourSum = tempSum.sum()
        if ourSum > 0:
            #for j in range(int(ourSum)):
            if np.random.uniform(0,1) < p:
                lattice[k,t-1] = 1
            else:
                lattice[k,t-1] = 0
           # else:
           #     lattice[k,t] = 
    if lattice[::,t-1].sum() > 0:
        return True
    else:
        return False

def update(ourLattice):
    ax.clear()
    ax.imshow(ourLattice, cmap = 'gray')

def pause(event):
    plt.pause(10000)

def resume(event):
    plt.gcf().canvas.stop_event_loop()


N = 200
prob = 0.53
ourLattice = lattice(N)

fig, ax = plt.subplots(figsize = (22,16))
plt.rcParams.update({'font.size':16})

#initializing the drawing


#creating the button (for stopping)
pauseButton = plt.axes([0.025, 0.4, 0.10, 0.10])
button = Button(pauseButton, 'Pause')
button.on_clicked(pause)

#creating the button (for resuming)
resetButton = plt.axes([0.025, 0.30, 0.10, 0.10])
startButton = Button(resetButton, 'Resume')
startButton.on_clicked(resume)
import time
for i in range(10000000):
    if plt.fignum_exists(1): #simply check if the figure exists,
        tf = directedUpdate(ourLattice, p = prob)
        if tf:
            if i % 5 == 0:
                ax.clear()
                update(ourLattice)
                #print(ourLattice)
                plt.pause(0.0001)
                plt.show(block=False)
                #else:
                #    plt.pause(25)
        else:
            break
#    plt.show(block = False)
#    plt.pause(0.1)
