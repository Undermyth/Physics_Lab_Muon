import waveform as wave
import numpy as np
import matplotlib.pyplot as plt

# num = 506
num = 19
filename = 'data/double_' + str(num) + '.csv'
args = {
    "time_line": 1e-7,
    "noise_threshold": 0.8,
    "max_peak_num"   : 8,
    "not_on_line"    : 1,
    "least_time"     : 1e-6,
    "most_time"      : 1e-5,
    "amplify_rate"   : 0.6,
    "least_main_peak": 2,
    "least_sub_peak" : 2
}
w = wave.waveform(**args)
w.y = np.loadtxt(filename)
w.process_data()
plt.plot(w.x, w.y)

for i in range(w.peaknum):
    if w.peaks[i]["has_second_peak"]:
        plt.scatter([w.peaks[i]["main_peak"][0], w.peaks[i]["second_peak"][0]], [w.peaks[i]["main_peak"][1], w.peaks[i]["second_peak"][1]], color = 'green')
        print(w.peaks[i]["second_peak"][0] - w.peaks[i]["main_peak"][0])
    else:
        plt.scatter([w.peaks[i]["main_peak"][0]], [w.peaks[i]["main_peak"][1]], color = 'blue')

plt.show()