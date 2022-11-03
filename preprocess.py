import matplotlib.pyplot as plt
import numpy as np

from peak_fix import fix_peak
from search import search as find_peak

x = np.arange(2500) * 4e-9
# p = 748
# y = np.loadtxt('data3/data' + str(p) + '.txt')

y = np.loadtxt('mock_data/data3/data456.txt')

peak_pos = find_peak(y)
peak_num = peak_pos[0]
print(peak_num)
real_peak_pos = np.empty(peak_num)
predict_peak = np.empty(peak_num)
for i in range(1, peak_num + 1):
    real_peak_pos[i - 1], predict_peak[i - 1] = fix_peak(x, y, min_pos = peak_pos[i], noise_threshold=0.1)

print(real_peak_pos)
print(predict_peak)

plt.plot(x, y)
plt.scatter(real_peak_pos, predict_peak, color = 'red')
plt.show()
