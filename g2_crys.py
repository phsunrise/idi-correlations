import numpy as np
from scipy import interpolate
from settings import basedir, a0_recip
import os, sys
import matplotlib.pyplot as plt

datadir = basedir + "crys/"
N_e = 1 # number of exposures per snapshot

Ihkls = np.load(datadir + "I_sum_%d.npz" % N_e)['Ihkls']
N_s = len(Ihkls) # number of snapshots
print "Number of snapshots =", N_s

# load K
K = np.load(datadir + "K.npy") 
N_pix = K.shape[0]*K.shape[1] # number of pixels

# calculate the Q values (= K1 - K2) 
K_flat = K.reshape(N_pix, 1, 3)
Q = []
for i in range(3):
    Q.append(K_flat[:,:,i] - K_flat[:,:,i].T)
Q = np.array(Q)
print "Q.shape =", Q.shape

Ihkl_ave = Ihkls.mean(axis=0)
Ihkls = (Ihkls - Ihkl_ave).reshape(N_s, N_pix)

G2 = np.tensordot(Ihkls, Ihkls, axes=(0, 0)) # this magically does what we want

G2avg = 1.*G2 / N_s
print "G2avg.shape =", G2avg.shape
np.savez(datadir + "G2avg_%d.npz"%N_e, G2avg=G2avg, Q=Q)

## generate another set of Q's
qx_n, qy_n = 301, 301
qx = np.linspace(-1.5, 1.5, qx_n) * a0_recip
qy = np.linspace(-1.5, 1.5, qy_n) * a0_recip
qz = 0.
q2d = np.array(np.meshgrid(qx, qy, qz, indexing='ij'))
q2d = q2d.reshape(3, np.prod(q2d.shape[1:])).transpose()

## sample on flat 2D plane
Q_flat = Q.reshape(3, np.prod(Q.shape[1:])).transpose()
G2_flat = G2avg.ravel()
G2_interp = interpolate.griddata(Q_flat[::5], G2_flat[::5], q2d)
G2_interp = G2_interp.reshape(qx_n, qy_n)
print "G2_interp.shape = ", G2_interp.shape
np.savez(datadir + "G2_interp_%d.npz"%N_e, G2_interp=G2_interp, \
         qx=qx, qy=qy, qz=qz)

plt.ion()
plt.imshow(G2_interp, interpolation='nearest')
plt.colorbar()
