from dataengine import dataengine
from waveform import waveform
import numpy as np
import matplotlib.pyplot as plt

# engine = dataengine(main_scale = '25E-6')
# xincr = engine.xincr
# print(xincr)
# wave = waveform(time_line = xincr)
datapath = './redata/'
# for i in range(1000):
#     engine.get_data(wave)
#     wave.save_waveform(datapath, 'data' + str(i) + '.csv')
#     print(i)

xincr = 1e-7
x = np.arange(2500) * xincr
y = np.loadtxt(datapath + 'data234.csv')
# plt.scatter(x, y, color = 'red')
plt.plot(x, y)
plt.show()

