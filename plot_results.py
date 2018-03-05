import numpy as np
import matplotlib.pyplot as plt
from settings import basedir
import os, sys
from getopt import getopt

datadir = basedir + "noncrys/"

do_readfile = False
filename = "g2_average.npy" # default filename

opts, args = getopt(sys.argv[1:], "r:s:")
for o, a in opts:
    if o == '-r':
        filename = a
        do_readfile = True
    elif o == '-s':
        filename = a

Q = np.load(datadir + "Q.npy")
Qnorm = np.sqrt(np.sum(Q**2, axis=0))
Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
N = len(Qnorm)

if do_readfile:
    try:
        g2 = np.load(datadir + filename)
    except IOError:
        print "%s not found! These are the available files:" \
                    % (datadir+filename)
        os.system("ls %s --ignore=\"g2_????.npy\" --ignore=\"Q.npy\"" \
                        % datadir)
        sys.exit(0)
else:
    i_f = 0
    g2 = np.zeros((N, N))
    while os.path.isfile(datadir + "g2_%04d.npy" % i_f):
        g2 += np.load(datadir + "g2_%04d.npy" % i_f)
        i_f += 1 
        if i_f % 100 == 0:
            print "read %d files" % i_f
    g2 = 1.*g2 / i_f
    print "\ntotal %d files" % i_f
    
    np.save(datadir + filename, g2)

print "# pixels = %d" % (g2.shape[0])

plt.figure()
plt.scatter(Qperp.ravel(), g2.ravel())

binned, bin_edges = np.histogram(Qperp.ravel(), \
                        bins=100, weights=g2.ravel())
counts, bin_edges = np.histogram(Qperp.ravel(), \
                        bins=100)
xx = 0.5*(bin_edges[:-1] + bin_edges[1:])
yy = 1.*binned / counts
plt.plot(xx, yy, 'r-')

#plt.figure()
#plt.plot(g2.ravel())
plt.show()
