import numpy as np
import scipy


def get_window(data, current, window_length):
    acc = data[0][current - window_length : current]
    gyro = data[1][current - window_length: current]
    mag = data[2][current - window_length: current]
    return acc, gyro, mag


# from a window of accelerometer data this function determines the share of free falling data points
def free_fall_score(acc):
    score = 0.0
    for v in acc:
        if np.linalg.norm(v) < 0.5:
            score += 1
    return score / len(acc)


def tumble_score(gyro):
    score = 0.0
    for v in gyro:
        if np.linalg.norm(v) > 1:
            score += 1
    return score / len(gyro)


def process(data, window_len, until):
    res = []
    for i in range(window_len):
        res.append(0)
    for i in range(window_len, until, 1):
        acc, gyro, mag = get_window(data, i, window_len)
        res.append(free_fall_score(acc) * tumble_score(gyro))
    return res




