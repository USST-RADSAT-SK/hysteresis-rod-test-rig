import numpy as np
import matplotlib.pyplot as plt

for n in range(32):
    n = 26
    data = np.genfromtxt(fname=f'Initial_Data\scope_{n}.csv', skip_header=2,  delimiter=',')
    valid = ~np.isnan(data[:, 1])
    data = data[valid, :]

    t = data[:, 0]
    v1 = data[:, 1]
    v2 = data[:, 2]

    dt = t[1] - t[0]
    intv2 = dt * (np.cumsum(v2) - 0.5 * v2[0] - 0.5 * v2)
    p = np.polyfit(t, intv2, 1)
    print(p)


    # plt.figure()
    # plt.plot(t, v1, label='Ch1')
    # plt.plot(t, v2, label='Ch2')
    # plt.plot(t, intv2, label='Ch2 integrated')
    # plt.plot(t, p[1] + p[0] * t)
    # plt.xlabel('Time (s)')
    # plt.ylabel('Voltage (V)')
    # plt.title('Stuff and things')
    # plt.legend()

    plt.figure()
    plt.title(n)
    plt.plot(v1, intv2 - p[1] - t * p[0])

    plt.show()
