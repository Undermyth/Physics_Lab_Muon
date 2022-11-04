from typing import Union
import numpy as np

from algorithm.peak_fix import fix_peak
from algorithm.search import search as search_peak
from algorithm.search_double_peak import find_double_peak

class waveform:

    def __init__(self, time_line: Union[str, np.ndarray], 
                noise_threshold: float = 0.8, search_scale: int = 10, max_peak_num: int = 8,
                peak_width: int = 10, not_on_line: float = 1., sample_interval: float = 1e-7):
        
        if isinstance(time_line, str):
            xincr = float(time_line)
            self.x = np.arange(2500) * xincr
        else:
            self.x = time_line

        self.max_peak_num = max_peak_num
        self.noise_threshold = noise_threshold
        self.search_scale = search_scale
        self.peak_width = peak_width
        self.not_on_line = not_on_line
        self.sample_interval = sample_interval

        peak = np.dtype([('main_peak', np.ndarray, 2), ('has_second_peak', np.bool_), ('second_peak', np.ndarray, 2)])
        self.peaks = np.empty(self.max_peak_num, dtype = peak)

    def getdata(self, data_from_engine: np.ndarray):
        self.y = data_from_engine
    
    def process_data(self):
        
        peak_pos = search_peak(self.y)
        peak_num = peak_pos[0]
        for i in range(1, peak_num + 1):
            self.peaks[i - 1]["main_peak"][0], self.peaks[i - 1]["main_peak"][1] = fix_peak(self.x, self.y, 
                                                                                            min_pos = peak_pos[i],
                                                                                            noise_threshold = self.noise_threshold,
                                                                                            not_on_line = self.not_on_line,
                                                                                            sample_interval = self.sample_interval
                                                                                            )
            double_peak = find_double_peak(self.x, self.y, 
                                            minpos = peak_pos[i],
                                            search_scale = self.search_scale,
                                            peak_width = self.peak_width,
                                            noise_threshold = self.noise_threshold,
                                            not_on_line = self.not_on_line
                                            )
            self.peaks[i - 1]["has_second_peak"] = False if double_peak == None else True
            if (self.peaks[i - 1]["has_second_peak"]):
                self.peaks[i - 1]["second_peak"][0], self.peaks[i - 1]["second_peak"][1] = fix_peak(self.x, self.y,
                                                                                                    min_pos = double_peak,
                                                                                                    noise_threshold = self.noise_threshold,
                                                                                                    not_on_line = self.not_on_line,
                                                                                                    sample_interval = self.sample_interval
                                                                                                    )
