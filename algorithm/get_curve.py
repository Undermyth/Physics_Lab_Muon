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
    sample_x = x[minpos + 1]
    sample_y = y[minpos + 1]
    if sample_y >= 0:
        sample_x = x[minpos]
        sample_y = y[minpos]
    lny = np.log(-sample_y)
    b = lny - a * sample_x
    return b


