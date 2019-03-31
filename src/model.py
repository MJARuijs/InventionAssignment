import numpy as np
import scipy

test_data = np.matrix('0 10 20 30 40 50 60 70 80;'
                      '1 11 21 31 41 51 61 71 81;'
                      '2 12 22 32 42 52 62 72 82;'
                      '3 13 23 33 43 53 63 73 83;'
                      '4 14 24 34 44 54 64 74 84;'
                      '5 15 25 35 45 55 65 75 85;'
                      '6 16 26 36 46 56 66 76 86;'
                      '7 17 27 37 47 57 67 77 87;'
                      '8 18 28 38 48 58 68 78 88;'
                      '9 19 29 39 49 59 69 79 89')

wl = 10;
base_down_dir = [1, 0, 0]
base_n = 0


def get_window(data, current, window_length):
    window = data[current - window_length : current]
    acc = window[:,0:3]
    gyro = window[:, 3:6]
    mag = window[:,6:9]
    return acc, gyro, mag


def main(data):
    curr_down = base_down_dir
    for i in range( wl, len(data), 1):
        acc, gyro, mag = get_window(data, i, wl)


a, g, m = get_window(test_data, 7, 3)

print a
print g
print m








