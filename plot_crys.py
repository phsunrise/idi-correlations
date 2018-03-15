import matplotlib.pyplot as plt
import numpy as np
from settings import basedir, a0_recip, colors
datadir = basedir + "crys/"

plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

N_es = [1, 10, 100, 1000]
for i_e, N_e in enumerate(N_es):
    f = np.load(datadir + "G2_interp_%d.npz" % N_e)
    qx = f['qx'] / a0_recip # unit: rlu
    qx_low, qx_high = 0.5*qx[0]-1.5*qx[1], 0.5*qx[-1]-1.5*qx[-2]
    qy = f['qy'] / a0_recip
    qy_low, qy_high = 0.5*qy[0]-1.5*qy[1], 0.5*qy[-1]-1.5*qy[-2]
    G2 = f['G2_interp']

    Ihkls = np.load(datadir + "I_sum_%d.npz" % N_e)['Ihkls']
    Iavg = np.mean(Ihkls)
    
#    fig3, ax3 = plt.subplots(1, 1, figsize=(7,7))
#    ax3.imshow(G2, origin='lower', \
#               extent=[qx_low, qx_high, qy_low, qy_high], \
#               interpolation='nearest')
#    ax3.set_xlabel(r"$Q_x$ (rlu)")
#    ax3.set_ylabel(r"$Q_y$ (rlu)")
#    fig3.savefig("plots/G2_interp_Nph_0p1_Nexp_%d_Nsnap_100.eps"%N_e)
#    fig3.savefig("plots/G2_interp_Nph_0p1_Nexp_%d_Nsnap_100.png"%N_e)
#    plt.close(fig3)

    offset = len(N_es) - 1. - i_e
    color = colors[i_e]
    ax1.plot(qx, G2[50, :]/Iavg**2*N_e + offset, color=color, \
             label=str(N_e))
    ax1.annotate("N=%d"%N_e, xy=(qx[190], offset+0.2), color=color)
    ax2.plot(qy, G2[:, 50]/Iavg**2*N_e + offset, color=color, \
             label=str(N_e))
    ax2.annotate("N=%d"%N_e, xy=(qx[190], offset+0.2), color=color)

ax1.set_xlabel(r"$Q_x$ (rlu)")
ax1.set_title(r"$Q_y = -1~\mathrm{(rlu)}$")
#ax1.legend()

ax2.set_xlabel(r"$Q_y$ (rlu)")
ax2.set_title(r"$Q_x = -1~\mathrm{(rlu)}$")
#ax2.legend()

fig.savefig("plots/G2_interp_Nph_0p1_Nsnap_100_comparison.eps")
fig.savefig("plots/G2_interp_Nph_0p1_Nsnap_100_comparison.png")
