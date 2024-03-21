import numpy as np
from numba import njit, prange
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


#here we define our random walk initialization
@njit()
def walk_initialization(N, steps = 10000):
    return np.zeros((N,steps))

#now we define walk update time step
@njit(parallel = True)
def walk_update(walkers, currentStep, t = 1, p = 0.50):
    #first we find the row we should enter.
    N = walkers.shape[0] 
    for k in range(t):
        for i in prange(N):
            if np.random.uniform(0,1) < p:
                walkers[i, currentStep] = walkers[i, currentStep-1] + 1
            else:
                walkers[i, currentStep] = walkers[i, currentStep-1] - 1
    return walkers

def update(ourWalkers, step):
    ax.clear()
    print(step)
    print(ourWalkers[::,0:step].T.shape)
    ax.plot(ourWalkers[::,0:step].T)

def pause(event):
    plt.pause(10000)

def resume(event):
    plt.gcf().canvas.stop_event_loop()


N = 100
prob = 0.50
time = 1000
ourWalkers = walk_initialization(N, steps = time)

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
step = 0
for i in range(10000000):
    if plt.fignum_exists(1): #simply check if the figure exists,
        step += 1
        tf = walk_update(ourWalkers, currentStep = step, p = prob)
        if i % 1 == 0:
            ax.clear()
            update(ourWalkers, step)
            #print(ourLattice)
            plt.pause(0.0001)
            plt.show(block=False)
            #else:
            #    plt.pause(25)
    else:
        break
#    plt.show(block = False)
#    plt.pause(0.1)
