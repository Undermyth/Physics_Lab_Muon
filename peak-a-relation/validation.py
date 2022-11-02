'''
    validate the accuracy for paramter a.
'''
import matplotlib.pyplot as plt
import numpy as np

pic = 230
noise_threshold = 0.8
fitpoints = 17
a = -2106906.394745603

x = np.arange(2500) * 4e-9
y = np.loadtxt('../data3/data' + str(pic) + '.txt')
reduced_x = x[::25]
reduced_y = y[::25]

minpos = np.argmin(reduced_y)
start = minpos
while np.abs(reduced_y[start] - reduced_y.min()) <= noise_threshold:
    start += 1
end = start
counter = 0
while np.abs(reduced_y[end]) >= noise_threshold and counter <= fitpoints:
    end += 1
    counter += 1
sample_x = reduced_x[start: end]
sample_y = reduced_y[start: end]
lny = np.log(-sample_y)
# b = np.average(lny) - a * np.average(sample_x)
b = lny[0] - a * sample_x[0]
def f(x):
    return -np.exp(a * x + b)

minpos = np.argmin(y)
plt.plot(x, y)
plt.scatter(reduced_x[start: end], reduced_y[start: end], color = 'red')
plt.plot(x[minpos - 30: minpos + 100], f(x[minpos - 30: minpos + 100]), 'g')
plt.show()
