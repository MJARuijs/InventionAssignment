import numpy as np


# A function which cuts a window out of the IMU data and returns it as three different matrices
# param data - the IMU data from which the window is to be cut out
# param current - the last point of the window
# param window_len - the size of the window
# return - A tuple containing three matrices of equal size containing the accelerometer, gyroscope, and magnetometer
# data
def get_window(data, current, window_len):
    acc = data[0][current - window_len : current]
    gyro = data[1][current - window_len: current]
    mag = data[2][current - window_len: current]
    return acc, gyro, mag


# A function which determines the share of free falling data points from a window of accelerometer data
# param acc - the 3d accelerometer data to be analysed
# return - the number of data points where the device appears to be in free fall divided by the total number of data
# points
def free_fall_score(acc):
    score = 0.0
    for v in acc:
        if np.linalg.norm(v) < 0.5:
            score += 1
    return score / len(acc)


# A function which determines the share of significantly tumbling data points from a window of gyroscope data
# param gyro - the 3d gyroscope data to be analysed
# return - the number of data points where the device tumbles significantly divided by the total number of data points
def tumble_score(gyro):
    score = 0.0
    for v in gyro:
        if np.linalg.norm(v) > 1:
            score += 1
    return score / len(gyro)


# A function which processes the IMU data and gives for each window a score between 0 and 1 which says how likely it is
# that the device is
# param data - the IMU data to be analysed
# param window_len - the size of the window used to determine the free fall and tumble scores
# param until - the point in the data at which the algorithm should stop analysing
# return - a list containing the score for each point in the data
def process(data, window_len, until):
    res = []
    # initial zero padding
    for i in range(window_len):
        res.append(0)
    # determining the score for each window
    for i in range(window_len, until, 1):
        acc, gyro, mag = get_window(data, i, window_len)
        res.append(free_fall_score(acc) * tumble_score(gyro))
    return res




