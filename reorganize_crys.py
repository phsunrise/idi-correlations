import numpy as np
import sys, os
from settings import basedir

datadir = basedir + "crys/"
N_es = [1, 10, 50, 100, 500, 1000] # number of exposures per snapshot
N_s = 100 # number of snapshots

for N_e in N_es:
    i_f = 0 # file counter
    while os.path.isfile(datadir + "I_%04d.npy" % i_f):
        if i_f == 0:
            Ihkls = np.load(datadir + "I_0000.npy")
        else:
            Ihkls = np.vstack((Ihkls, \
                        np.load(datadir + "I_%04d.npy" % i_f)))

        if len(Ihkls) >= N_s * N_e: 
            break
        
        i_f += 1

    shapex, shapey = Ihkls.shape[1], Ihkls.shape[2]
    Ihkls = Ihkls[:(N_s*N_e)].reshape(N_e, N_s, shapex, shapey).sum(axis=0)

    np.savez(datadir + "I_sum_%d.npz" % (N_e), N_e=N_e, Ihkls = Ihkls)
    print "Done N_e =", N_e
