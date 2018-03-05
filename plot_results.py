import numpy as np
import matplotlib.pyplot as plt
from settings import basedir
import os, sys

datadir = basedir + "noncrys/"

Q = np.load(datadir + "Q.npy")
Qnorm = np.sqrt(np.sum(Q**2, axis=0))
Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
N = len(Qnorm)

i_f = 0
g2 = np.zeros((N, N))
while os.path.isfile(datadir + "g2_%04d.npy" % i_f):
    g2 += np.load(datadir + "g2_%04d.npy" % i_f)
    i_f += 1 
    if i_f % 100 == 0:
        print "read %d files" % i_f
g2 = 1.*g2 / i_f
print "total %d files" % i_f

print "# pixels = %d" % (g2.shape[0])

plt.figure()
plt.scatter(Qperp.ravel(), g2.ravel())

plt.figure()
plt.plot(g2.ravel())
plt.show()
