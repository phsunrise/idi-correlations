import numpy as np
import matplotlib.pyplot as plt
from settings import basedir
import os, sys
from Sq_iso import Sq_iso_2D

do_compare = 'Np' # 'Np'=Nparticles or 'Ne'=Nexposures
plt.ion()

if do_compare == 'Ne':
    N_p = 10
    N_a = 6. * N_p
    datadir = basedir + "noncrys/2D_N_%d/" % (N_p)

    if len(sys.argv) == 1:
        nums = ['100', '500', '1000', '5000']
    else:
        nums = sys.argv[1:]

    Q = np.load(datadir + "Q.npy")
    Qnorm = np.sqrt(np.sum(Q**2, axis=0))
    Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
    N_pix = len(Qnorm)

    Nbins = 100
    xx = np.zeros(Nbins)
    for num in nums:
        G2 = np.load(datadir + "G2_average_%s.npy" % num)
        mask = np.eye(N_pix).astype(bool)
        G20 = np.sum(G2[mask]) * (1./N_pix) # G2(q=0)
        g2 = G2 / G20
        binned, bin_edges = np.histogram(Qperp.ravel(), \
                                bins=Nbins, weights=g2.ravel())
        counts, bin_edges = np.histogram(Qperp.ravel(), \
                                bins=Nbins)
        xx = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        yy = 1. * binned / counts
        if num == '5000':
            print "G2(q=0) = ", G20
            yy_all = yy
            #plt.scatter(Qperp.ravel(), g2.ravel(), alpha=0.3)
        num_shots = 100 * int(num)
        plt.plot(xx[1:], yy[1:], '-', label=str(num_shots))

    yy = (N_a**2 + Sq_iso_2D(xx, N_p) - N_a) / (2.*N_a**2 - N_a)
    plt.plot(xx[1:], yy[1:], '-', label=r"$\infty$")

    #from scipy.stats import linregress
    #_xx = (N_a + Sq_iso_2D(xx, N_p)) / (N_a + Sq_iso_2D(0., N_p))
    #slope, intercept, r_val, _, _ = linregress(_xx[30:70], yy_all[30:70])
    #print slope, intercept, r_val
    #yy = slope*_xx+intercept
    #plt.plot(xx[1:], yy[1:], '-', label=r"$\infty_\mathrm{fit}$")

    #plt.ylim(0.485, 0.530)
    plt.legend()

    plt.figure()
    plt.plot(xx[1:-1], (yy-yy_all)[1:-1])


elif do_compare == 'Np':
    N_ps = [1, 10, 30, 100]
    Nbins = 100
    num = 100 # usually in [100, 500, 1000, 5000]
              # 100*num is the number of exposures
    for N_p in N_ps:
        N_a = 6. * N_p
        datadir = basedir + "noncrys/2D_N_%d/" % (N_p)

        Q = np.load(datadir + "Q.npy")
        Qnorm = np.sqrt(np.sum(Q**2, axis=0))
        Qperp = np.sqrt(np.sum(Q[:2, :, :]**2, axis=0))
        N_pix = len(Qnorm)

        xx = np.zeros(Nbins)
        G2 = np.load(datadir + "G2_average_%d.npy" % num)
        mask = np.eye(N_pix).astype(bool)
        G20 = np.sum(G2[mask]) * (1./N_pix) # G2(q=0)
        g2 = G2 / G20
        binned, bin_edges = np.histogram(Qperp.ravel(), \
                                bins=Nbins, weights=g2.ravel())
        counts, bin_edges = np.histogram(Qperp.ravel(), \
                                bins=Nbins)
        xx = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        yy = 1. * binned / counts
        if num == '5000':
            print "G2(q=0) = ", G20
            yy_all = yy
            #plt.scatter(Qperp.ravel(), g2.ravel(), alpha=0.3)
        num_shots = 100 * num
        plt.plot(xx[1:], (2.*yy[1:]-1.)*N_p, '-', label=r"$N_p=%d$"%N_p)

        #yy = (N_a**2 + Sq_iso_2D(xx, N_p) - N_a) / (2.*N_a**2 - N_a)
        #plt.plot(xx[1:], yy[1:], '-', label=r"$\infty$")

        #from scipy.stats import linregress
        #_xx = (N_a + Sq_iso_2D(xx, N_p)) / (N_a + Sq_iso_2D(0., N_p))
        #slope, intercept, r_val, _, _ = linregress(_xx[30:70], yy_all[30:70])
        #print slope, intercept, r_val
        #yy = slope*_xx+intercept
        #plt.plot(xx[1:], yy[1:], '-', label=r"$\infty_\mathrm{fit}$")

        #plt.ylim(0.485, 0.530)

    plt.legend()
    plt.xlabel(r"$Q_\perp$")
    plt.ylabel(r"$N_p\times (|S(Q_\perp)/S(0)|^2 -1)$")
    plt.ylim(-0.25, 1.25)
    plt.savefig("plots/noncrys_noPoisson.eps")
    plt.savefig("plots/noncrys_noPoisson.png")

    #plt.figure()
    #plt.plot(xx[1:-1], (yy-yy_all)[1:-1])
