import dataengine as dm
import waveform as wave
import matplotlib.pyplot as plt
import numpy as np

dms = dm.dataengine(main_scale = '25E-6')
xincr = dms.xincr
# xincr = 1e-7
args = {
    "noise_threshold": 0.8,
    "max_peak_num": 8,
    "not_on_line": 1,
    "least_time": 5e-7,
    "most_time": 2e-5,
    "amplify_rate": 0.6,
    "flat_length": 30
}
w = wave.waveform(time_line = xincr, **args)
save_counter = 0
muon_counter = 0
counter = 0
double_counter = 0
for i in range(100000):
    dms.get_data(w)
    try:
        w.process_data()
        counter += 1
        muon_counter += w.peaknum
    except:
        print('process error.')
        continue
    for j in range(w.peaknum):
        try:
            tmp = w.peaks[j]
            save_counter += 1
            w.save_waveform('./rererere/', 'double' + str(save_counter) + '.csv')
            if tmp["has_second_peak"]:
                double_counter += 1
                save_counter += 1
                w.save_waveform('./rererere/', 'double' + str(save_counter) + '.csv')
        except:
            print('count error.')
    print(f'counter: {counter}. moun_counter: {muon_counter}. double_counter: {double_counter}.\n')

            

    
# plt.plot(w.x, w.y)
# plt.scatter(w.x, w.y)
# for i in range(w.peaknum):
#     tmp = w.peaks[i]
#     if tmp["has_second_peak"]:
#         plt.scatter([tmp["main_peak"][0], tmp["second_peak"][0]], [tmp["main_peak"][1], tmp["second_peak"][1]], color = 'red')
#     else:
#         plt.scatter([tmp["main_peak"][0]], [tmp["main_peak"][1]], color = 'blue')
# plt.show()

# 102 flat
# 760 ?

