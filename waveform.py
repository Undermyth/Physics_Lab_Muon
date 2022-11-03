from typing import Union
import numpy as np

class waveform:

    def __init__(self, time_line: Union[str, np.ndarray], max_peak_num: int = 8):
        
        if isinstance(time_line, str):
            xincr = float(time_line)
            self.x = np.arange(2500) * xincr
        else:
            self.x = time_line

        self.max_peak_num = max_peak_num

        peak = np.dtype([('main_peak', np.ndarray, 2), ('has_second_peak', np.bool_), ('second_peak', np.ndarray, 2)])
        self.peaks = np.empty(self.max_peak_num, dtype = peak)

    def getdata(self, data_from_engine: np.ndarray):
        self.y = data_from_engine
    
    def process_data():
        pass