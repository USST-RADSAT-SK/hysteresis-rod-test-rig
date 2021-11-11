# Hysteresis rod test rig Data Checking out 
# Date - 25th october, 2021
# Authors - Lukas, Atharva

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(fname='Initial_Data\scope_1.csv', skip_header=2,  delimiter= ',')
valid = ~np.isnan(data[:, 1])
data = data[valid, :]

t = data[:, 0]
v1 = data[:, 1]
v2 = data[:, 2]

plt.figure()
plt.plot(t, v1, label='Ch1')
plt.plot(t, v2, label='Ch2')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Stuff and things')
plt.legend()
plt.show()


print(data)