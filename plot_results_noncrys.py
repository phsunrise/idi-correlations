import numpy as np
from settings import basedir
import os, sys
from getopt import getopt

datadir = basedir + "noncrys/"

do_readfile = False
filename = "G2_average.npy" # default filename
MaxFile = np.iinfo(np.int32).max # default maximum number of files
do_batch = False

opts, args = getopt(sys.argv[1:], "r:s:n:bh")
for o, a in opts:
    if o == '-r': # read certain file
        filename = a
        do_readfile = True
    elif o == '-s': # save as certain file
        filename = a
    elif o == '-n': # maximum number of files
        MaxFile = int(a)
    elif o == '-b': # batch mode
        do_batch = True
    elif o == '-h': # help message
        print "Options:"
        print "-r [filename]: read from file"
        print "-s [filename]: save as file"
        print "-n [number N]: read at most N files"
        print "-b: batch mode"
        sys.exit(0)

Q = np.load(datadir + "Q.npy")
Qnorm = np.sqrt(np.sum(Q**2, axis=0))
Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
N = len(Qnorm)

if do_readfile:
    try:
        G2 = np.load(datadir + filename)
    except IOError:
        print "%s not found! These are the available files:" \
                    % (datadir+filename)
        os.system("ls %s --ignore=\"G2_????.npy\" --ignore=\"Q.npy\"" \
                        % datadir)
        sys.exit(0)
else:
    i_f = 0
    G2 = np.zeros((N, N))
    while os.path.isfile(datadir + "G2_%04d.npy" % i_f) and i_f < MaxFile:
        G2 += np.load(datadir + "G2_%04d.npy" % i_f)
        i_f += 1 
        if i_f % 100 == 0:
            print "read %d files" % i_f
    G2 = 1.*G2 / i_f
    print "\ntotal %d files" % i_f
    
    np.save(datadir + filename, G2)

print "# pixels = %d" % (G2.shape[0])

if not do_batch:
    import matplotlib.pyplot as plt
    plt.figure()
    plt.scatter(Qperp.ravel(), G2.ravel())

    binned, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=100, weights=G2.ravel())
    counts, bin_edges = np.histogram(Qperp.ravel(), \
                            bins=100)
    xx = 0.5*(bin_edges[:-1] + bin_edges[1:])
    yy = 1.*binned / counts
    plt.plot(xx, yy, 'r-')

    #plt.figure()
    #plt.plot(G2.ravel())
    plt.show()
