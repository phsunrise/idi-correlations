import numpy as np
import matplotlib.pyplot as plt
from settings import basedir
import os, sys
from Sq_iso import Sq_iso_2D

N_particles = 10
N_atoms = 6.*N_particles
datadir = basedir + "noncrys/2D_N_%d/" % (N_particles)
#datadir = basedir + "noncrys/"

if len(sys.argv) == 1:
    nums = ['100', '500', '1000', '5000']
else:
    nums = sys.argv[1:]

Q = np.load(datadir + "Q.npy")
Qnorm = np.sqrt(np.sum(Q**2, axis=0))
Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
N_pix = len(Qnorm)

Nbins = 100
xx = np.zeros(Nbins)
for num in nums:
    G2 = np.load(datadir + "G2_average_%s.npy" % num)
    mask = np.eye(N_pix).astype(bool)
    G20 = np.sum(G2[mask]) * (1./N_pix) # G2(q=0)
    g2 = G2 / G20
    binned, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=Nbins, weights=g2.ravel())
    counts, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=Nbins)
    xx = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    yy = 1. * binned / counts
    if num == '5000':
        print "G2(q=0) = ", G20
        yy_all = yy
        #plt.scatter(Qperp.ravel(), g2.ravel(), alpha=0.3)
    num_shots = 100 * int(num)
    plt.plot(xx[1:], yy[1:], '-', label=str(num_shots))

yy = (N_atoms**2 + Sq_iso_2D(xx, N_particles) - N_atoms) / (2.*N_atoms**2 - N_atoms)
plt.plot(xx[1:], yy[1:], '-', label=r"$\infty$")

#from scipy.stats import linregress
#_xx = (N_atoms + Sq_iso_2D(xx, N_particles)) / (N_atoms + Sq_iso_2D(0., N_particles))
#slope, intercept, r_val, _, _ = linregress(_xx[30:70], yy_all[30:70])
#print slope, intercept, r_val
#yy = slope*_xx+intercept
#plt.plot(xx[1:], yy[1:], '-', label=r"$\infty_\mathrm{fit}$")

#plt.ylim(0.485, 0.530)
plt.legend()

plt.figure()
plt.plot(xx[1:-1], (yy-yy_all)[1:-1])

plt.show()
