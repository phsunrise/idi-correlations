import numpy as np
import matplotlib.pyplot as plt
from idi_str_factors import idi_str_factors_noncrys
from Sq_iso import Sq_iso_2D

q = np.linspace(0., 2., 100, endpoint=False) + 2./100/2
N_particles = 2 

Q = np.zeros((100,1,3))
Q[:,0,0] = q

Ihkl = np.zeros(100)
N_e = 1000 
for i_e in range(N_e):
    fhkl = idi_str_factors_noncrys(Q, dim='2D', N=N_particles, do_CDI=True)
    Ihkl += np.abs(fhkl.reshape(100))**2
    if i_e % 100 == 0:
        print "done %d" % i_e

Ihkl = Ihkl / N_e
plt.plot(q, Ihkl, label=str(N_e))

yy = Sq_iso_2D(q, N_particles)
plt.plot(q, yy, label=r"$\infty$")

#from scipy.stats import linregress
#slope, intercept, r_val, _, _ = linregress(yy[30:70], Ihkl[30:70])
#print slope, intercept, r_val
#yy = slope*yy + intercept
#plt.plot(q, yy, '-', label=r"$\infty_\mathrm{fit}$")

plt.legend()

plt.figure()
plt.plot(q, Ihkl-yy)

plt.show()
