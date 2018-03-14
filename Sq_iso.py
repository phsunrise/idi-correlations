import numpy as np
from scipy.special import jn

'''
now implementing 2D case only
see writeup for details
'''

def Sq_iso_2D(q, N): # N = number of particles, not atoms
    if isinstance(q, np.ndarray):
        is_array = True
    else:
        is_array = False
        q = np.array([q])

    a = 12. * np.sin(np.pi/5.)
    b = 12. * np.sin(np.pi*2./5.)
    L = 1000. # box size

    #rho0_term = np.zeros(len(q))
    #mask = q < 1.e-8
    #rho0_term[mask] = 6.*(N-1.)
    #rho0_term[~mask] = 0.*6.*(N-1.) * (2./L/q[~mask]*np.sin(L/2.*q[~mask]))**2

    Sq = (N+2) * (6. + 10.*jn(0, 6.*q) + 10.*jn(0, a*q) + 10.*jn(0, b*q))
    #print Sq

    if is_array:
        return Sq
    else:
        return float(Sq)
