# Hysteresis rod test rig data processing
# Date - 26th November, 2021
# Authors - Lukas

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

freq = 1

if freq == 10:
    indices = (1, 11)
elif freq == 50:
    indices = (11, 22)
elif freq == 1:
    indices = (33, 38)



for i in range(*indices):

    data = np.genfromtxt(fname=f'data-2021-11-26\scope_{i}.csv', skip_header=2,  delimiter= ',')
    valid = ~np.isnan(data[:, 1])
    data = data[valid, :]

    # if i == indices[0]:
    #     t = data[:, 0]
    #     v1 = data[:, 1]
    #     v2 = data[:, 2]
    # else:
    #     v1 += data[:, 1]
    #     v2 += data[:, 2]
    
    t = data[:, 0]
    v1 = data[:, 1]
    v2 = data[:, 2]
    plt.plot(t, v1)
    plt.show()

v1 /= indices[1] - indices[0]
v2 /= indices[1] - indices[0]

plot_verbose = False

if plot_verbose:
    plt.figure()
    plt.plot(t, v1)

if plot_verbose:
    plt.figure()
    plt.plot(t, v2)

# recenter the ch1 signal
v0 = np.average(v1)
v1 -= v0
if plot_verbose:
    plt.figure()
    plt.plot(t, v1)

# recenter the ch2 signal 
v0 = np.average(v2)  # -0.004024
v2 -= v0
if plot_verbose:
    plt.figure()
    plt.plot(t, v2)
# 
# integrate, recenter again
v2dt = np.array([0., *cumtrapz(v2, t)])
v2dt -= np.average(v2dt)
if plot_verbose:
    plt.figure()
    plt.plot(t, v2dt)

# plot B vs H (but actually just the proportional voltages)
if plot_verbose:
    plt.figure()
    plt.plot(v1, v2dt)

# convert to B and H
# H = n I = n V / R = (10000 turns/m) * (v1) / (456 Ohm)
H = 1e4 * v1 / 178.2  # A / m

# B = int(v2) / N2 S where N2 is the number of turns in the measuring coil and S is the cross section of the rod
# there would also be contributions from the generating coil but they are small (mu0 H ~ 10^-4)
B = v2dt / (5e-4**2 * np.pi) / 2929 # T

plt.figure()
plt.plot(H, B)
plt.xlabel('H (A/m)')
plt.ylabel('B (T)')





plt.show()
