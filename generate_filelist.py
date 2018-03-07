import numpy as np
import os, sys
from settings import basedir

datadir = basedir + "noncrys/"

total = 5000

filelist = []
for i in range(total):
    if not os.path.isfile(datadir + "G2_%04d.npy" % i):
        filelist.append(i)

print filelist

n = len(filelist)
print "total %d files" % n

nprocs = int(raw_input("number of processors: "))
sublists = [[] for i in range(nprocs)]
for i_f, f in enumerate(filelist):
    sublists[i_f % nprocs].append(f)

for i in range(nprocs):
    np.save("filelist_%03d.npy"%i, np.array(sublists[i]).astype(int))
