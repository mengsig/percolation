import numpy as np
import time

N = 10000000
counter = 0
t1 = time.time()
for i in range(N):
	x = np.random.uniform(0,1)
	y = np.random.uniform(0,1)
	d = x**2 + y**2
	if d < 1:
		counter += 1

t_python = time.time() - t1
print(f'Our estimate of Pi: {4*counter/N}') 
print(f'This computation took - {time.time() - t1} seconds')

t1 = time.time()

x = np.random.uniform(0,1,N)
y = np.random.uniform(0,1,N)
d = x**2 + y**2
d = d < 1
dSum = d.sum()

t_numpy = time.time() - t1
print(f'Our estimate of Pi: {4*dSum/N}') 
print(f'This computation took - {t_numpy} seconds')

from numba import njit, prange

@njit(parallel = True)
def estimate_pi(N):
	counter = 0
	for i in prange(N):
		x = np.random.uniform(0,1)
		y = np.random.uniform(0,1)
		if x**2 + y**2 < 1:
			counter += 1
	return counter

estimate_pi(10000)
t1 = time.time()
numbaCount = estimate_pi(N)
t_numba = time.time() - t1
print(f'Our estimate of Pi: {4*numbaCount/N}') 
print(f'This computation took - {t_numba} seconds')
print(' ')
print(f'Numpy was {t_python/t_numpy} times faster')
print(f'Numba was {t_python/t_numba} times faster')
print(f'\n If you use python instead of numba/compiled language, you are using a computer from year {int(2023-2*np.log(t_python/t_numba)/np.log(2))}.')
