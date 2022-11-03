'''
    obtain the final dropping time from processed data.
    print a, b, R^2 from the fit, and draw a plot.
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_excel('minvalue-k-relation.xlsx')
k = np.array(df['k'])
minval = np.array(df['minvalue'])
coef = np.polyfit(k, minval, deg = 1)
def f(x):
    return coef[0] * x + coef[1]
print(coef[0], coef[1])
y_average = np.average(minval)
R2 = 1 - np.sum((minval - f(k)) ** 2) / np.sum((minval - y_average) ** 2)
print(R2)
x = np.linspace(k.min(), k.max(), 100)
y = f(x)
plt.scatter(k, minval)
plt.plot(x, y, 'r')
plt.xlabel('tangent of descending(V)', fontsize=14)
plt.ylabel('peak volt(V/s)', fontsize=14)
plt.show()
