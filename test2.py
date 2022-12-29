import numpy as np
import matplotlib.pyplot as plt

num = 3

filename = 'data/double_' + str(num) + '.csv'
y = np.loadtxt(filename)
x = np.arange(2500) * 1e-7
plt.plot(x, y)

for p in range()