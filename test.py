import dataengine as dm
import waveform as wave
import matplotlib.pyplot as plt
import numpy as np

# dms = dm.dataengine(main_scale = '25E-6')
# xincr = dms.xincr
xincr = 1e-7
args = {
    "noise_threshold": 0.8,
    "max_peak_num": 8,
    "not_on_line": 1,
    "least_time": 1e-6,
    "most_time": 1e-5,
    "amplify_rate": 0.6
}
w = wave.waveform(time_line = xincr, **args)
# dms.get_data(w)
w.y = np.loadtxt('redata/zipped/data854.csv')
w.process_data()
plt.plot(w.x, w.y)
plt.scatter(w.x, w.y)
for i in range(w.peaknum):
    tmp = w.peaks[i]
    if tmp["has_second_peak"]:
        plt.scatter([tmp["main_peak"][0], tmp["second_peak"][0]], [tmp["main_peak"][1], tmp["second_peak"][1]], color = 'red')
    else:
        plt.scatter([tmp["main_peak"][0]], [tmp["main_peak"][1]], color = 'blue')
plt.show()

# 102 flat
# 760 ?

