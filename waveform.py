from typing import Union
import numpy as np

from algorithm.peak_fix import fix_peak
from algorithm.search import search as search_peak
from algorithm.combine_peak import combinepeak
from algorithm.datatype import peak

class waveform:

    def __init__(self, time_line: str, 
                noise_threshold: float = 0.8, 
                max_peak_num: int = 8, 
                not_on_line: float = 1.,
                least_time: float = 1e-6,
                most_time: float = 1e-5,
                amplify_rate: float = 0.6,
                flat_length: int = 30,
                least_main_peak: float = 2.0,
                least_sub_peak: float = 2.0):
        

        xincr = float(time_line)
        self.x = np.arange(2500) * xincr            # a string representing xincr. Is a string dur to the request of VISA format

        self.max_peak_num = max_peak_num            # how many peaks can appear in the same time
        self.noise_threshold = noise_threshold      # thredhold for noise
        self.not_on_line = not_on_line              # standard for point whether on the minus-exp
        self.sample_interval = xincr                # same as xincr
        self.least_time = least_time                # smallest time interval for double peak
        self.most_time = most_time                  # largest time interval for double peak
        self.amplify_rate = amplify_rate            # largest ratio for small_peak_height / large_peak_height
        self.flat_length = flat_length              # maximum length for flat peak
        self.least_main_peak = least_main_peak      # minimum height for main peak (used in search@chenke)(minus)
        self.least_sub_peak = least_sub_peak        # minimum height for sub peak (used in search@chenke)(minus)

        self.peaks = np.empty(self.max_peak_num, dtype = peak)

    def getdata(self, data_from_engine: np.ndarray):
        self.y = data_from_engine
    
    def process_data(self):
        
        peak_detected = search_peak(self.y, zV_ = -self.least_main_peak, tV_ = -self.least_sub_peak)

        self.peaks, peak_num = combinepeak(peak_detected, self.y,
                                            max_peak_num = self.max_peak_num,
                                            xincr = self.sample_interval,
                                            least_time = self.least_time,
                                            most_time = self.most_time,
                                            amplify_rate = self.amplify_rate,
                                            flat_length = self.flat_length)
        self.peaknum = peak_num
        for i in range(peak_num):
            self.peaks[i]["main_peak"][0], self.peaks[i]["main_peak"][1], self.peaks[i]["detected"] = fix_peak(self.x, self.y, 
                                                                                                            min_pos = self.peaks[i]["main_peak"][0],
                                                                                                            noise_threshold = self.noise_threshold,
                                                                                                            not_on_line = self.not_on_line,
                                                                                                            sample_interval = self.sample_interval
                                                                                                            )
            if self.peaks[i]["has_second_peak"]:
                self.peaks[i]["second_peak"][0], self.peaks[i]["second_peak"][1], _ = fix_peak(self.x, self.y, 
                                                                                        min_pos = self.peaks[i]["second_peak"][0],
                                                                                        noise_threshold = self.noise_threshold,
                                                                                        not_on_line = self.not_on_line,
                                                                                        sample_interval = self.sample_interval
                                                                                        )
    def save_waveform(self, savepath: str, filename: str):
        # print(savepath + filename)
        np.savetxt(savepath + filename, self.y)

# mock
if __name__ == '__main__':
    wave = waveform(time_line = '4E-9')
