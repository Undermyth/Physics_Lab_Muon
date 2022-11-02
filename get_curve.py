import json

import numpy as np

# API for get parameter a, b in
#   y = -exp(a * x + b)

def get_curve_a():
    with open('parameter.json') as f:
        paramter = json.load(f)
    return paramter['curve_a']

def get_curve_b(x, y, noise_threshold = 0.8):
    a = get_curve_a()
    minpos = np.argmin(y)
    start = minpos
    while np.abs(y[start] - y.min()) <= noise_threshold:
        start += 1
    sample_x = x[start]
    sample_y = y[start]
    lny = np.log(-sample_y)
    b = lny - a * sample_x
    return b


