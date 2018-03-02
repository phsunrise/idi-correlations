import numpy as np
np.random.seed(0)

'''
function to calculate S(Q)
input: Q, a 3d array of shape (ny, nx, 3)
output: fhkl, S(Q) of shape (ny, nx)
'''

def idi_str_factors(Q):
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
