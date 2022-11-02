'''
    get_tangent() will process a V-t plot to find the descending tangent.
    the tangent is returned as coef[0].
    in main(), it will process 1000 samples to prove that peakvalue is 
    linear with k, which implies that descending time is a constant.
    visualization is available.
'''

import numpy as np


def get_tangent(x, y, noise_threshold = 0.8, descending_threshold = 1, max_sample_num = 10):

    # find the start point of the descending line
    minpos = np.argmin(y)
    dropping = minpos
    ending = minpos
    while np.abs(y[dropping]) > noise_threshold:
        dropping -= 1
    
    # clear out redundant points within noise range
    while np.abs(y[dropping + 1] - y[dropping]) <= descending_threshold:
        dropping += 1
    while np.abs(y[ending - 1]  - y[ending]) <= descending_threshold:
        ending -= 1
    
    # do polyfit
    xsample = x[dropping: ending + 1]
    ysample = y[dropping: ending + 1]
    coef = np.polyfit(xsample, ysample, deg = 1)
    
    # return tangent
    return coef[0], dropping, ending    # dropping and ending are added just for debug. Should be removed.

# mock
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.arange(1250) * 8e-9
    k = np.empty(1000)
    min_value = np.empty(1000)
    start = np.empty(1000)
    end = np.empty(1000)

    for i in range(1000):
        y = np.loadtxt('../data3/data' + str(i) + '.txt')
        k[i], start[i], end[i] = get_tangent(x, y[::2])
        min_value[i] = y[::2].min()

    # save data for further process
    # np.savetxt('ki.csv', -k)
    # np.savetxt('minvalue.csv', -min_value)

    # plt.plot(np.arange(190), k)
    plt.scatter(-min_value, -k)
    plt.xlabel('peak_value(absolute)')
    plt.ylabel('tangent of descending(absolute)')
    plt.xlim(0, 60)
    plt.show()
