'''
    do fitting for the minus-exp curve.
    in main(), 1000 samples were tested to show that
    in U = -exp(a * t + b), a remains nearly constant.
'''
import numpy as np


def curve(x, y, fitpoints = 250, noise_threshold = 0.8):
    
    # decide the points used to fit
    minpos = np.argmin(y)
    start = minpos
    while np.abs(y[start] - y.min()) <= noise_threshold:
        start += 1
    end = start
    counter = 0
    while np.abs(y[end]) >= noise_threshold and counter <= fitpoints:
        end += 1
        counter += 1
    sample_x = x[start: end]
    sample_y = y[start: end]

    # do fit
    coef = np.polyfit(sample_x, np.log(-sample_y), deg = 1)
    return coef[0], start, end, y.min()    # return start and end only for debug

def minus_exp(x, coef):
    return -np.exp(coef[0] * x + coef[1])

# mock
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    a = np.empty(1000)
    start = np.empty(1000)
    end = np.empty(1000)
    minval = np.empty(1000)
    x = np.arange(2500) * 4e-9
    for i in range(1000):
        y = np.loadtxt('../data3/data' + str(i) + '.txt')
        a[i], start[i], end[i], minval[i] = curve(x, y)
    
    # debug
    # pic = 200
    # start = start.astype(np.int32)
    # end = end.astype(np.int32)
    # y = np.loadtxt('../data3/data' + str(pic) + '.txt')
    # print(start[pic], end[pic])
    # plt.scatter(x[start[pic]: end[pic]], y[start[pic]: end[pic]], color = 'red')
    # plt.plot(x, y)

    # save data for further process
    # np.savetxt('rank.csv', np.arange(1000))
    # np.savetxt('minval.csv', minval)
    # np.savetxt('curve.csv', a)

    plt.scatter(minval, a)
    plt.show()

