'''
    this file is to show that the dropping time
    obtained by the linear relation is accurate.
'''

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(2500) * 4e-9
y = np.loadtxt('../data3/data123.txt')
minpos = np.argmin(y)
dropping = minpos
while np.abs(y[dropping]) >= 0.8:
    dropping -= 1
peak = x[dropping] + 4.7084304680613126e-08
ytick = np.arange(-50, 0)
plt.plot(x, y)
plt.plot([peak] * len(ytick), ytick, 'g--')
plt.show()
