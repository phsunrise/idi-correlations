'''
python version of MATLAB code by Mariano Trigo
'''
import numpy as np
import matplotlib.pyplot as plt
from outgoingks import K, Omega
from idi_str_factors import idi_str_factors_crys
from settings import basedir 
from getopt import getopt
import os, sys

fileind = 0
datadir = basedir + "crys/"

opts, args = getopt(sys.argv[1:], "f:h")
for o, a in opts:
    if o == '-f': # file index 
        fileind = int(a)
    elif o == '-h':
        print "Options:"
        print "-f [FILE INDEX]: save file to FILE INDEX"
        sys.exit(0)

if fileind == 0:
    np.save(datadir + "K.npy", K)
#print K.shape
N_pix = K.shape[0]*K.shape[1] # number of pixels

'''
# calculate the Q values (= K1 - K2) 
K_flat = K.reshape(N_pix, 1, 3)
Q = []
for i in range(3):
    Q.append(K_flat[:,:,i] - K_flat[:,:,i].T)
Q = np.array(Q)
'''

## ensemble average
N0_e = 1000 # each file contains N0_e exposures
Ihkls = []

for i_e in range(N0_e):
    fhkl = idi_str_factors_crys(K, n = 0.01)
    Ihkl = np.abs(fhkl)**2 * Omega/(4.*np.pi)
    Ihkl = np.random.poisson(Ihkl) # add Poisson noise
    Ihkls.append(Ihkl.astype(float))

    #plt.imshow(Ihkl, interpolation = 'nearest')
    #plt.colorbar()
    #plt.show()

    if i_e % 100 == 0:
        print "done %d" % i_e

#    Ihkl_flat = np.abs(fhkl.reshape(N_pix, 1))**2
#
#    ### look at speckle pattern
#    #plt.imshow(np.abs(fhkl)**2)
#    #plt.colorbar()
#    #plt.show()
#    #sys.exit(0)
#
#    G2 = G2 + Ihkl_flat.dot(Ihkl_flat.T)
#
#G2avg = 1.*G2 / N0_e
#np.save(datadir + "G2_%04d.npy" % (i_f), G2avg)

np.save(datadir + "I_%04d.npy" % fileind, Ihkls)
