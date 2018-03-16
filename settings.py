import numpy as np
import matplotlib.pyplot as plt

basedir = "/scratch/users/phsun/idi/"
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# For crystalline simulation
a0 = 3. # lattice constant in Angstrom
a0_recip = 2.*np.pi / a0

