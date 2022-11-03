import json

import numpy as np
from scipy.optimize import fsolve

from check_shape import checkshape
from get_curve import get_curve_a, get_curve_b

# fix the peak of low rate sampling. 
# return the position(not index) of the peak.

def fix_peak(x, y, min_pos = -1, noise_threshold = 0.8, not_on_line = 1, sample_interval = 1e-7):

    # definition for return value.
    return_peakpos = 0
    return_peak = 0

    # preparation: get the curve and load parameters.
    with open('parameter.json') as f:
        parameter = json.load(f)
    dropping_time = parameter['dropping_time']
    a = get_curve_a()
    b = get_curve_b(x, y, outer_min_pos = min_pos, noise_threshold = noise_threshold)
    def curve(x):
        return -np.exp(a * x + b)

    # first get the situation of the figure from checkshape().
    coord, have_point_on_descending = checkshape(x, y,
                                                outer_minpos = min_pos,
                                                noise_threshold = noise_threshold,
                                                not_on_line = not_on_line,
                                                sample_interval = sample_interval)
    
    print(have_point_on_descending)     # debug
    
    # if not have point on the descending, then approximate the peak directly.
    minpos = min_pos if min_pos != -1 else np.argmin(y)
    if not have_point_on_descending:
        peak_pos = coord + dropping_time
        return_peakpos, return_peak = peak_pos, curve(peak_pos)
    
    # if have point on the descending, then we will solve an equation.
    else:
        mid_x = x[coord]
        mid_y = y[coord]
        def equation(x):
            return [curve(x[1]) * (mid_x - x[0]) - mid_y * (x[1] - x[0]), x[1] - x[0] - dropping_time]
        root = fsolve(equation, [x[minpos] - dropping_time, x[minpos]])
        return_peakpos, return_peak = root[1], curve(root[1])

    # final check. If the minimum value of y is still smaller than return_peak, 
    # then it's better to use the original peak, not the predicted one.
    if y[minpos] < return_peak:
        return x[minpos], y[minpos]
    else:
        return return_peakpos, return_peak

# mock
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    y = np.loadtxt('mock_data/data3/data412.txt')
    x = np.arange(2500) * 4e-9
    reduced_x = x[::25]
    reduced_y = y[::25]
    peak_pos, peak = fix_peak(reduced_x, reduced_y)

    a = get_curve_a()
    b = get_curve_b(reduced_x, reduced_y)
    def curve(x):
        return -np.exp(a * x + b)
    y_tick = np.linspace(-30, 0, 50)
    minpos = np.argmin(y)
    plt.plot(x, y)
    plt.plot(x[minpos - 30: minpos + 100], curve(x[minpos - 30: minpos + 100]), 'y')
    plt.plot([peak_pos] * len(y_tick), y_tick, 'g--')
    plt.scatter(reduced_x, reduced_y, color = 'red')
    plt.scatter([peak_pos], [peak], color = 'green')
    plt.show()
