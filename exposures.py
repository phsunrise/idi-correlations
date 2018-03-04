'''
python version of MATLAB code by Mariano Trigo
'''
import numpy as np
import matplotlib.pyplot as plt
from outgoingks import outgoingks
from idi_str_factors import idi_str_factors_crys, idi_str_factors_noncrys
from settings import basedir 

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
np.save(datadir + "Q.npy", Q)

## ensemble average
N_e = 1000 # number of exposures 
N0_e = 10 # average over every N0_e exposures
for i_f in range(N_e/N0_e):
    g2avg = np.zeros((N_pix, N_pix))
    for i_e in range(N0_e):
        fhkl = idi_str_factors_noncrys(K)
        Ihkl_flat = np.abs(fhkl.reshape(N_pix, 1))**2
        g2avg = g2avg + Ihkl_flat.dot(Ihkl_flat.T)
    g2avg = 1.*g2avg / N0_e
    np.save(datadir + "g2_%04d.npy" % (i_f), g2avg)
    print "done %d/%d" % (i_f+1, N_e/N0_e)
