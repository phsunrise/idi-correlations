import numpy as np
from scipy.special import jn

'''
now implementing 2D case only
see writeup for details
'''

def Sq_iso_2D(q):
    if isinstance(q, np.ndarray):
        is_array = True
    else:
        is_array = False
        q = np.array([q])

    a = 12. * np.sin(np.pi/5.)
    b = 12. * np.sin(np.pi*2./5.)
    L = 1000. # box size

    mask = q < 1.e-10
    if np.sum(~mask):
        rho0_term = 594. * (2./L/q[~mask]*np.sin(L/2.*q[~mask]))**2 + \
                    594. * mask
    else:
        rho0_term = 594. * mask

    Sq = 10./6. * jn(0, 6.*q) + 10./6. * jn(0, a*q) + \
         10./6. * jn(0, b*q) + rho0_term 

    if is_array:
        return Sq
    else:
        return float(Sq)
