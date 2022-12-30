import numpy as np
import os
import waveform as wave
import warnings
import math

'''
    when data collection is completed, this function can be called to
    do multichannel analyze and lifetime calculation.

    datapath: directory for dataset to be analysed. according to the 
    requirementsin UI.py@chenke, the name of file in the specified 
    directory should be in the form double_xxx.csv.
    
    ***ATTENTION***: datapath should end with '/'.

    channels: the number of channels for multichannel process.
    max_main(sub)_height: the maximum acceptable peak height for main 
    peak and second peak, respectively. (positive)

'''
def analyse(datapath: str, 
            channels: int, 
            max_main_height: float, 
            max_sub_height: float,
            **waveargs):

    if datapath[-1] != '/':
        warnings.warn("analyser.py: `datapath` should end with /.", SyntaxWarning)

    main_bucket = np.zeros(channels)
    sub_bucket = np.zeros(channels)
    main_width = max_main_height / channels
    sub_width = max_sub_height / channels
    main_bucket_13731 = np.zeros(channels)
    sub_bucket_13731 = np.zeros(channels)
    kernel = np.array([1,3,7,3,1])
    average_life = 0
    count = 0

    dirs=os.listdir(datapath)
    dirs=[i for i in dirs if len(i.split('.'))>1 and len(i.split('_'))>1 and i.split('.')[1]=="csv"]

    for f in dirs:

        # debug
        # print(">", f)

        w = wave.waveform(**waveargs)
        y = np.loadtxt(datapath + f, dtype = np.float32)
        w.y = y
        w.process_data()

        for i in range(w.peaknum):
            if w.peaks[i]["has_second_peak"]:

                main_height = -w.peaks[i]["main_peak"][1]
                sub_height = -w.peaks[i]["second_peak"][1]
                life = w.peaks[i]["second_peak"][0] - w.peaks[i]["main_peak"][0]
                main_index = math.floor(main_height / main_width)
                sub_index  = math.floor(sub_height / sub_width)
                main_index = channels - 1 if main_index > channels - 1 else main_index
                sub_index  = channels - 1 if sub_index > channels - 1 else sub_index

                main_bucket[main_index] += 1
                sub_bucket[sub_index] += 1
                average_life += life
                count += 1

    # 1-3-7-3-1 wave filtering 
    kernel = np.array([1, 3, 7, 3, 1])
    main_bucket_13731 = np.convolve(main_bucket, kernel, 'same')
    sub_bucket_13731  = np.convolve(sub_bucket,  kernel, 'same')
    '''
    main_bucket=np.pad(main_bucket,(2,2),'constant')
    sub_bucket=np.pad(sub_bucket,(2,2),'constant')

    main_bucket_13731=np.array([(main_bucket[i-2:i+3]*kernel).sum() for i in range(2, channels + 2)])
    sub_bucket_13731=np.array([(sub_bucket[i-2:i+3]*kernel).sum() for i in range(2, channels + 2)])
    '''
    '''
    for i in range(2, channels - 2):
        main_bucket_13731[i] = 1 * main_bucket[i - 2] + 3 * main_bucket[i - 1] + 7 * main_bucket[i] + 3 * main_bucket[i + 1] + 1 * main_bucket[i + 2]
        sub_bucket_13731[i] = 1 * sub_bucket[i - 2] + 3 * sub_bucket[i - 1] + 7 * sub_bucket[i] + 3 * sub_bucket[i + 1] + 1 * sub_bucket[i + 2]
    
    main_bucket_13731[0]            = main_bucket[0]
    main_bucket_13731[1]            = main_bucket[1]
    main_bucket_13731[channels - 2] = main_bucket[channels - 2]
    main_bucket_13731[channels - 1] = main_bucket[channels - 1]

    sub_bucket_13731[0]            = sub_bucket[0]
    sub_bucket_13731[1]            = sub_bucket[1]
    sub_bucket_13731[channels - 2] = sub_bucket[channels - 2]
    sub_bucket_13731[channels - 1] = sub_bucket[channels - 1]
    '''
    average_life /= count

    return main_bucket_13731, sub_bucket_13731, average_life, count

# mock
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文

    waveargs = {
        "time_line": 1e-7,
        "noise_threshold": 0.8,
        "max_peak_num": 8,
        "not_on_line": 1,
        "least_time": 1e-6,
        "most_time": 1e-5,
        "amplify_rate": 0.6,
        "least_main_peak": 2,
        "least_sub_peak": 2
    }

    mainbucket, subbucket, avtime, count = analyse(datapath = './data/', channels = 1024, max_main_height = 100, max_sub_height = 30, **waveargs)
    # mainbucket = np.arange(256)
    # subbucket = np.arange(256)

    b1 = plt.bar(np.arange(1024), mainbucket, color = 'orange')
    # b2 = plt.bar(np.arange(256), subbucket, color = 'blue')

    # plt.legend([b1, b2], [r"$\mu$"+"子能量分布", "电子能量分布"])
    print(avtime, count)
    plt.show()
