import numpy as np

'''
function to calculate S(Q)
input: Q, a 3d array of shape (ny, nx, 3)
output: fhkl, S(Q) of shape (ny, nx)
Note that for IDI, Q is actually K (= k_out)
'''

def idi_str_factors_crys(Q):
    ## 3D lattice of random emitters
    sc_numat = 20 # number of atoms in each dimension
    N = sc_numat ** 3 # total number of atoms
    a0 = 1. # lattice constant, in angstrom
    rndphases = 2.*np.pi*np.random.random_sample((N,))

    _xx = np.arange(sc_numat) * a0
    _yy = np.arange(sc_numat) * a0
    _zz = np.arange(sc_numat) * a0
    rs = np.meshgrid(_xx, _yy, _zz, indexing='ij')
    rs = np.array(rs).reshape(3, N)
        # rs[0], rs[1], rs[2] are x,y,z coordinates of the atoms

    ## compute S(Q)
    fhkl = np.sum(np.exp(1.j * (Q.dot(rs) + rndphases)), \
                  axis=2)

    return fhkl

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


def idi_str_factors_noncrys(Q, dim='2D', N=10, do_CDI=False):
    '''
    N = number of particles (not atoms)
    If do_CDI = True, don't do random phases
    '''
    # define particle: star-shaped 
    positions = [[0., 0., 0.]]
    bl = 6. # bond length in angstrom
    for i in range(5):
        positions.append([bl*np.cos(i*2.*np.pi/5.), \
                          bl*np.sin(i*2.*np.pi/5.), 0.])
    positions = np.array(positions).T

    #box_size = np.array([1000., 1000., 1000.]) # angstrom, in [x,y,z] directions
    box_size = np.array([100., 100., 100.]) # angstrom, in [x,y,z] directions
    # the box is centered at the origin

    # initialize particles 
    coords = np.random.random_sample((N, 3))*box_size - box_size/2.
    angles = np.random.random_sample((N, 3))*[2.*np.pi, 2.*np.pi, np.pi]
    if dim == '2D':
        coords[:, 2] = 0. # set z coords to 0
        angles[:, 0] = 0.
        angles[:, 2] = 0. # only phi is nonzero

    # calculate atom positions
    # rs[0], rs[1], rs[2] are x,y,z coordinates of the atoms
    rs = calc_positions(positions, \
            coords[0, 0], coords[0, 1], coords[0, 2], \
            angles[0, 0], angles[0, 1], angles[0, 2])
    for i_p in range(N-1):
        rs = np.hstack((rs, \
                calc_positions(positions, \
                coords[i_p, 0], coords[i_p, 1], coords[i_p, 2], \
                angles[i_p, 0], angles[i_p, 1], angles[i_p, 2])))

    #import matplotlib.pyplot as plt
    #from mpl_toolkits.mplot3d import Axes3D
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(rs[0], rs[1], rs[2])
    #ax.set_aspect('equal')
    #plt.show()

    if not do_CDI:
        rndphases = 2.*np.pi*np.random.random_sample((N*6,))

        ## compute S(Q)
        fhkl = np.sum(np.exp(1.j * (Q.dot(rs) + rndphases)), \
                      axis=-1)
    else:
        fhkl = np.sum(np.exp(1.j * Q.dot(rs)), axis=-1)

    return fhkl
