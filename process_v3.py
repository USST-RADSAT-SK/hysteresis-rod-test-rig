# Hysteresis rod test rig data processing
# Date - 27th November, 2021
# Authors - Lukas

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

# maps frequencies to the corresponding range of data files
indices = {
    10: (101, 110),
    20: (111, 120),
    50: (121, 130),
    100: (131, 140)
}

Rx = 45.9

plot_verbose = False
for freq in [10, 20, 50, 100]:

    for i in range(*indices[freq]):

        data = np.genfromtxt(fname=f'data-2021-11-27\scope_{i}.csv', skip_header=2,  delimiter= ',')
        valid = ~np.isnan(data[:, 1])
        if freq == 50:
            blip = [98, 99, 100, 101, 102, 498, 499, 500, 501, 502, 898, 899, 900, 901, 902]
            valid[blip] = False
        data = data[valid, :]



        if i == indices[freq][0]:
            t = data[:, 0]
            v1 = data[:, 1]
            v2 = data[:, 2]

            # plt.plot(t, v1)
            # plt.plot(t, v2)
            # plt.show()
        else:
            v1 += data[:, 1]
            v2 += data[:, 2]
            # plt.plot(t, data[:, 1])
            # plt.plot(t, data[:, 2])
            # plt.show()


    v1 /= indices[freq][1] - indices[freq][0]
    v2 /= indices[freq][1] - indices[freq][0]

    if plot_verbose:
        plt.figure(2)
        plt.plot(t, v1)

    if plot_verbose:
        plt.figure(3)
        plt.plot(t, v2)

    # recenter the ch2 signal 
    v0 = np.average(v2)  # -0.004024
    if freq == 50:
        v0 += 0.04
    v2 -= v0
    if plot_verbose:
        plt.figure(4)
        plt.plot(t, v2)
    # 
    # integrate, recenter again
    v2dt = np.array([0., *cumtrapz(v2, t)])
    v2dt -= np.average(v2dt)
    if plot_verbose:
        plt.figure(5)
        plt.plot(t, v2dt)

    # plot B vs H (but actually just the proportional voltages)
    if plot_verbose:
        plt.figure(6)
        plt.plot(v1, v2dt)

    # convert to B and H
    # H = n I = n V / R = (10000 turns/m) * (v1) / (456 Ohm)
    H = 1e4 * v1 / Rx  # A / m

    # B = int(v2) / N2 S where N2 is the number of turns in the measuring coil and S is the cross section of the rod
    # there would also be contributions from the generating coil but they are small (mu0 H ~ 10^-4)
    # negated because terminals must have been hooked up backwards
    B = -v2dt / (5e-4**2 * np.pi) / 2929 # T

    plt.figure(1)
    plt.plot(H, B, label=f'{freq} Hz', zorder=-freq)
    plt.xlabel('H (A/m)')
    plt.ylabel('B (T)')

plt.legend()
plt.show()
