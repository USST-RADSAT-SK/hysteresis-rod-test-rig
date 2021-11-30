# Hysteresis rod test rig data processing
# Date - 25th November, 2021
# Authors - Lukas

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz


for i in range(1, 7):  # samples 1-6 correspond to the straight rod at 10 Hz, our best potential signal

    data = np.genfromtxt(fname=f'Initial_Data\scope_{i}.csv', skip_header=2,  delimiter= ',')
    valid = ~np.isnan(data[:, 1])
    data = data[valid, :]

    if i == 1:
        t = data[:, 0]
        v1 = data[:, 1]
        v2 = data[:, 2]
    else:
        v1 += data[:, 1]
        v2 += data[:, 2]

v1 /= 6.0
v2 /= 6.0

print(min(v1), max(v1))

# plt.figure(1)
# plt.plot(t, v1, label=i)

# plt.figure(2)
# plt.plot(t, v2, label='Ch2')

# recenter the ch2 signal 
v0 = np.average(v2)  # -0.004024
v2 -= v0
# plt.figure(3)

# integrate, recenter again
v2dt = np.array([0., *cumtrapz(v2, t)])
v2dt -= np.average(v2dt)
# plt.figure(4)
# plt.plot(t, v2dt)

# plot B vs H (but actually just the proportional voltages)
# plt.figure(5)
# plt.plot(v1, v2dt)

# convert to B and H
# H = n I = n V / R = (10000 turns/m) * (v1) / (456 Ohm)
H = 1e4 * v1 / 456  # A / m

# B = int(v2) / N2 S where N2 is the number of turns in the measuring coil and S is the cross section of the rod
# there would also be contributions from the generating coil but they are small (mu0 H ~ 10^-4)

B = v2dt / (5e-4**2 * np.pi) / 2929 # T
plt.figure(6)
plt.plot(H, B)
plt.xlabel('H (A/m)')
plt.ylabel('B (T)')





plt.show()
