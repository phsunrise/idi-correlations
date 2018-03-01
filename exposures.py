'''
python version of MATLAB code by Mariano Trigo
'''
import numpy as np
from outgoingqs import outgoingqs

## setup
geometry = {}
geometry['lambda0'] = 0.8 # angstrom
ny, nz = 30, 30
geometry['imageNy'] = ny
geometry['imageNy'] = nz

geometry['beam_center'] = [1691./2., 1691./2.]
geometry['det_name'] = 'CSPAD'
geometry['det_pixels_horz'] = 1692
geometry['det_size_vert'] = 186.0100
geometry['det_pixels_vert'] = 1691
geometry['det_dist'] = 80.
geometry['det_size_horz'] = 186.12

## generate Q vectors corresponding to each detector pixel
## note that here Q = k_out, not k_out - k_in
Q = outgoingqs(geometry)
Qflat = Q.reshape(Q.shape[0]*Q.shape[1], 3:) 

## ensemble average
