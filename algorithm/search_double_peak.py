from typing import Union
import numpy as np
from .get_curve import get_curve_a, get_curve_b

def find_double_peak(x: np.ndarray, y: np.ndarray, minpos: Union[None, int],
                    search_scale: int = 50, peak_width: int = 10,
                    noise_threshold: float = 0.8, not_on_line: float = 1) -> Union[None, int]:
    
    min_pos = np.argmin(y) if minpos == None else minpos
    a = get_curve_a()
    b = get_curve_b(x, y, outer_min_pos = minpos, noise_threshold = noise_threshold)
    def minus_exp(x):
        return -np.exp(a * x + b)
    
    # searching for double peak
    find_double = False
    for i in range(search_scale):
        prediction = minus_exp(x[min_pos + i])
        if (np.abs(prediction - y[min_pos + i]) > not_on_line):
            find_double = True
            break
    
    if find_double:

        # determine the position of approximate double peak
        double_peak_pos = np.argmin(y[i: i + peak_width])
        return double_peak_pos

    else:
        return None
