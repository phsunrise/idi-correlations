import sys, os
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt

N = 10 # number of particles
dim = '2D'
N_s = 100 # number of snapshots

box_size = np.array([1000., 1000., 1000.]) # angstrom, in [x,y,z] directions
# the box is centered at the origin

def calc_positions(positions_inside, x, y, z, psi, phi, theta):
    '''
    function returning the atom positions in each particle
    the particle is treated as a rigid body
    http://mathworld.wolfram.com/EulerAngles.html
    '''
    C1, S1 = np.cos(psi), np.sin(psi)
    C2, S2 = np.cos(phi), np.sin(phi)
    C3, S3 = np.cos(theta), np.sin(theta)
    rot = np.array([[ C1*C2-C3*S2*S1,  C1*S2+C3*C2*S1, S1*S3],\
                    [-S1*C2-C3*S2*C1, -S1*S2+C3*C2*C1, C1*S3],\
                    [S3*S2,           -S3*C2,          C3]])
    return rot.dot(positions_inside) + np.array([[x], [y], [z]]) 

# define particle: star-shaped, bond length = 3 angstrom
positions = [[0., 0., 0.]]
for i in range(5):
    positions.append([3.*np.cos(i*2.*np.pi/5.), \
                      3.*np.sin(i*2.*np.pi/5.), 0.])
positions = np.array(positions).T

for i_s in range(N_s):
    # initialize particles 
    coords = np.random.random_sample((N, 3))*box_size - box_size/2.
    angles = np.random.random_sample((N, 3))*[2.*np.pi, 2.*np.pi, np.pi]
    if dim == '2D':
        coords[:, 2] = 0. # set z coords to 0
        angles[:, 0] = 0.
        angles[:, 2] = 0. # only phi is nonzero

    # calculate atom positions
    all_positions = calc_positions(positions, \
            coords[i_p, 0], coords[i_p, 1], coords[i_p, 2], \
            angles[i_p, 0], angles[i_p, 1], angles[i_p, 2])
    for i_p in range(N-1):
        all_positions = np.hstack((all_positions, \
                calc_positions(positions, \
                coords[i_p, 0], coords[i_p, 1], coords[i_p, 2], \
                angles[i_p, 0], angles[i_p, 1], angles[i_p, 2])))
    all_positions = all_positions.T

