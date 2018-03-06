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
print "total %d files" % len(filelist)
