import numpy as np
import matplotlib.pyplot as plt

f = np.load("results.npz")
g2 = f['g2']
print "# pixels = %d" % (g2.shape[0])

plt.figure()
plt.plot(g2.ravel())

plt.figure()
plt.plot(g2.ravel()[:2000])
plt.show()
