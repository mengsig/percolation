This is a repository for visualization purposes of percolation, complex physics, phase transisitons, etc..

This will be a continuous work in progress, but the following things are included as of today. Please note that the simulations corresponding to points 2 and 3 take a bit to initialize, on my PC it takes around 8seconds for 1000x1000 grid (sparse matrix of 1.000.000 nodes/pixels).

	1. 2D lattice - random and uniform percolation with visualization and sliding bar for $\alpha$, along with a resetting button to the critical value for the system. This has been implemented using networkx, and displays the links.
	2. 2D lattice - random and  uniform percolation with visualization (imshow) for extremely fast visualization (but without links). Implemented using sparse matrices and sparse graph routines for coloring purposes. As of now, I havent found a good solution for the coloring scheme.
	3. 2D lattice - uniform percolation with temporal visualization of increasing and decreasing probability of removing links (here the probability is oscillating between [0,1]). The temporal visualization can be linear or based on a normal distribution around the critical value of the function (to slow down time around this). Note that the maximum recommended resolution is N = 2500 --> 6.250.000 million (nodes) or pixels on the screen. NOTE: here you must press CTRL-C afterwards to cancel the infinte loop that exists. 
	4. 2D lattice - here we have the same as in point 3., however, in this part we also have added another figure that displays the probability density function of the connected compenents (cluster) sizes. 

By Marcus Engsig
22/08/2023.
