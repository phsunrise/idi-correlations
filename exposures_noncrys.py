'''
python version of MATLAB code by Mariano Trigo
'''
import numpy as np
import matplotlib.pyplot as plt
from outgoingks import outgoingks
from idi_str_factors import idi_str_factors_crys, idi_str_factors_noncrys
from settings import basedir 
from getopt import getopt
import os, sys

do_filelist = False
filelist = np.arange(100).astype(int)
opts, args = getopt(sys.argv[1:], "f:h")
for o, a in opts:
    if o == '-f': # read filelist
        do_filelist = True
        filelist = np.load(a).astype(int)
    elif o == '-h':
        print "Options:"
        print "-s [START NUM]: start saving from START NUM"
        print "-f [FILELIST]: read file list from file FILELIST"
        sys.exit(0)

## setup
geometry = {}
geometry['lambda0'] = 0.8 # angstrom
ny, nz = 30, 30
geometry['imageNy'] = ny
geometry['imageNz'] = nz

geometry['beam_center'] = [1691./2., 1691./2.]
geometry['det_name'] = 'CSPAD'
geometry['det_pixels_horz'] = 1692
geometry['det_size_vert'] = 186.0100
geometry['det_pixels_vert'] = 1691
geometry['det_dist'] = 80.
geometry['det_size_horz'] = 186.12

## generate K vectors corresponding to each detector pixel
## note that here K = k_out, not k_out - k_in
K = outgoingks(geometry)
N_pix = K.shape[0]*K.shape[1] # number of pixels

# calculate the Q values (= K1 - K2) 
K_flat = K.reshape(N_pix, 1, 3)
Q = []
for i in range(3):
    Q.append(K_flat[:,:,i] - K_flat[:,:,i].T)
Q = np.array(Q)

datadir = basedir + "noncrys/"

## ensemble average
N0_e = 100 # each file is an average over every N0_e exposures
for i_f in filelist:
    if i_f == 0:
        np.save(datadir + "Q.npy", Q)
    G2 = np.zeros((N_pix, N_pix))
    for i_e in range(N0_e):
        fhkl = idi_str_factors_noncrys(K, dim = '2D')
        Ihkl_flat = np.abs(fhkl.reshape(N_pix, 1))**2

        ### look at speckle pattern
        #plt.imshow(np.abs(fhkl)**2)
        #plt.colorbar()
        #plt.show()
        #sys.exit(0)

        G2 = G2 + Ihkl_flat.dot(Ihkl_flat.T)

    G2avg = 1.*G2 / N0_e
    np.save(datadir + "G2_%04d.npy" % (i_f), G2avg)
    print "done file %d" % (i_f)
