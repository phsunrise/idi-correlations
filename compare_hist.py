import numpy as np
import matplotlib.pyplot as plt
from settings import basedir
import os, sys
from Sq_iso import Sq_iso_2D

datadir = basedir + "noncrys/"

nums = sys.argv[1:]

Q = np.load(datadir + "Q.npy")
Qnorm = np.sqrt(np.sum(Q**2, axis=0))
Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
N_pix = len(Qnorm)

# get G2(Q=0)
mask = np.eye(N_pix).astype(bool)
G2 = np.load(datadir + "G2_average_5000.npy")
G20 = np.sum(G2[mask]) * (1./N_pix)

Nbins = 100
xx = np.zeros(Nbins)
for num in nums:
    g2 = np.load(datadir + "G2_average_%s.npy" % num)/G20
    binned, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=Nbins, weights=g2.ravel())
    counts, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=Nbins)
    xx = 0.5*(bin_edges[:-1] + bin_edges[1:])
    yy = 1.*binned / counts
    plt.plot(xx, yy, '-', label=num)

yy = (Sq_iso_2D(xx) / Sq_iso_2D(0.)) ** 2
plt.plot(xx, yy, '-', label=r"$\infty$")

plt.ylim(0.48, 0.52)
plt.legend()
plt.show()
