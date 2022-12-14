import numpy as np
from .datatype import peak

def combinepeak(peak_detected: np.ndarray, y: np.ndarray, max_peak_num: int = 8, 
                xincr: float = 4e-9, least_time: float = 5e-7, most_time: float = 10e-6, amplify_rate: float = 0.6,
                flat_length: int = 30):

    # convert peak_detected(which is generated by search@chenke) into flat array
    peak_seq = []
    for entry in peak_detected:
        it = iter(entry)
        peak_num = next(it)
        for k in range(peak_num):
            peak_seq.append(next(it))

    peaks = np.empty(max_peak_num, dtype = peak)
    peak_count = 0

    i = 0
    while i < len(peak_seq):
        try:
            after = i + 1
            while (y[peak_seq[after]] == y[peak_seq[after - 1]] and peak_seq[after] - peak_seq[after - 1] < flat_length): after += 1
            i_now = after
            after = peak_seq[after]
        except IndexError:
            # there is no peak left
            peaks[peak_count]["main_peak"][0] = peak_seq[i]
            peaks[peak_count]["main_peak"][1] = y[peak_seq[i]]
            peaks[peak_count]["has_second_peak"] = np.False_
            peak_count += 1
            break
        
        # if: 1) the interval is longer than 1us and less than 10us;
        #     2) the amplitude of the second peak is less than 60% of the main peak;
        # then we think it is a muon.

        index_of_i = peak_seq[i]
        # debug
        # print((after - index_of_i) * xincr > least_time)
        # print((after - index_of_i) * xincr < most_time)
        # print(abs(y[after]) < amplify_rate * abs(y[index_of_i]))
        if (after - index_of_i) * xincr > least_time and (after - index_of_i) * xincr < most_time and abs(y[after]) < amplify_rate * abs(y[index_of_i]):
            peaks[peak_count]["main_peak"][0] = index_of_i
            peaks[peak_count]["main_peak"][1] = y[index_of_i]
            peaks[peak_count]["has_second_peak"] = np.True_
            peaks[peak_count]["second_peak"][0] = after
            peaks[peak_count]["second_peak"][1] = y[after]
            peak_count += 1
            i = i_now + 1
        
        # otherwise, it's a single peak
        else:
            peaks[peak_count]["main_peak"][0] = index_of_i
            peaks[peak_count]["main_peak"][1] = y[index_of_i]
            peaks[peak_count]["has_second_peak"] = np.False_
            peak_count += 1
            i = i_now
    
    return peaks, peak_count



    
    

