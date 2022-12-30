import numpy as np

peak = np.dtype([('main_peak', np.ndarray, 2), ('has_second_peak', np.bool_), ('second_peak', np.ndarray, 2), ('detected', np.bool_)])