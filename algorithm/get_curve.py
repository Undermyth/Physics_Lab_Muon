import json
from typing import Union
import numpy as np

# API for get parameter a, b in
#   y = -exp(a * x + b)

def get_curve_a():
    with open('parameter.json') as f:
        paramter = json.load(f)
    return paramter['curve_a']

def get_curve_b(x: np.ndarray, y: np.ndarray, outer_min_pos: Union[None, float], noise_threshold: float = 0.8):
    a = get_curve_a()
    # minpos = outer_min_pos if outer_min_pos != -1 else np.argmin(y)
    minpos = np.argmin(y) if outer_min_pos == None else outer_min_pos
    start = minpos
    while np.abs(y[start] - y[minpos]) <= noise_threshold:
        start += 1
    sample_x = x[start]
    sample_y = y[start]
    lny = np.log(-sample_y)
    b = lny - a * sample_x
    return b


