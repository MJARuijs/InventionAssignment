import numpy as np
import scipy


def get_window(data, current, window_length):
    window = data[current - window_length : current]
    acc = window[:,0:3]
    gyro = window[:, 3:6]
    mag = window[:,6:9]
    return acc, gyro, mag








