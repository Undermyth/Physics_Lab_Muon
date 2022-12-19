from typing import Union
import json

import numpy as np

from .get_curve import get_curve_a, get_curve_b

# check the shape of y. Value returned could be:
# if a point on the descending side is detected, then return the index and signal True.
# if no point is detected to be on the descending side, then return the fixed position 
# of approximate dropping point and signal False.
# The approximation will be made by finding the point just before descending, and ret-
# urn the x position of the point plus a small fixation.

def checkshape(x: np.ndarray, y: np.ndarray, outer_minpos: Union[None, float], noise_threshold = 0.8, not_on_line = 1, sample_interval = 1e-7):

    # parameter preparation.
    with open('parameter.json') as f:
        parameter = json.load(f)

    # searching begin with the lowest point.
    minpos = np.argmin(y) if outer_minpos == None else outer_minpos

    # rule 1: if the line goes up two times on the left, then minpos - 1 is on the des-
    # cending side.
    if np.abs(y[minpos - 2] - y[minpos - 1]) > noise_threshold:
        # print('fit rule 1')     # debug
        return minpos - 1, True
    
    # rule 2: if the lowest point is far from the minus-exp curve which is fitted, then
    # the lowest point is on the descending side.
    a = get_curve_a()
    b = get_curve_b(x, y, outer_min_pos = outer_minpos, noise_threshold = noise_threshold)
    def minus_exp(x):
        return -np.exp(a * x + b)
    
    # check the distance from the lowest point.
    predict_lowest = minus_exp(x[minpos])
    if np.abs(predict_lowest - y[minpos]) > not_on_line:
        # print('fit rule 2. predicted lowest = ', predict_lowest)     # debug
        return minpos, True
    
    # rule 3: if nothing above happened, then the point just before descending can be a 
    # approximation. Since the point always appears before descending, fixation of half
    # the expected distance from the ideal descending point will be added.
    dropping_time = parameter['dropping_time']
    fixation = (sample_interval - dropping_time) / 2
    # print('fit rule 3')     # debug
    return x[minpos - 1] + fixation, False

# mock
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    y = np.loadtxt('mock_data/data3/data230.txt')
    x = np.arange(2500) * 4e-9
    reduced_x = x[::25]
    reduced_y = y[::25]
    coord, have_point_on_descending = checkshape(reduced_x, reduced_y)
    plt.plot(x, y)
    plt.scatter(reduced_x, reduced_y, color = 'green')
    if have_point_on_descending:
        plt.scatter([reduced_x[coord]], [reduced_y[coord]], color = 'red')
    else:
        plt.scatter([coord], [0], color = 'red')
    plt.show()
