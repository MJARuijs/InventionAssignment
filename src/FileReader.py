import os
import glob
import numpy as np


def read_files(path, file_name):
    folder = os.getcwd() + path
    absolute_path = glob.glob(folder + file_name)

    delay = 0
    count = 0
    acc_data = np.zeros(0)
    mag_data = np.zeros(0)
    gyro_data = np.zeros(0)

    all_data = []

    for f in absolute_path:
        start_index = f.rfind('/') + 1
        with open(f) as file_data:
            content = ''
            for line in file_data:
                content += line

            segments = content.split('~')

            for segment in segments:
                lines = segment.split('\n')

                if segment[0] == 'D':
                    delay = int(lines[0][1:])
                if segment[0] == 'A':
                    count = int(lines[0][1:])
                    acc_data = np.zeros(3 * count).reshape([count, 3])
                    for i in range(0, count):
                        acc_data[i] = np.fromstring(lines[i + 1], sep=' ')
                elif segment[0] == 'G':
                    count = int(lines[0][1:])
                    gyro_data = np.zeros(3 * count).reshape([count, 3])
                    for i in range(0, count):
                        gyro_data[i] = np.fromstring(lines[i + 1], sep=' ')
                elif segment[0] == 'M':
                    count = int(lines[0][1:])
                    mag_data = np.zeros(3 * count).reshape([count, 3])
                    for i in range(0, count):
                        mag_data[i] = np.fromstring(lines[i + 1], sep=' ')
            all_data.append([delay, count, acc_data, mag_data, gyro_data, f[start_index:len(f)]])
    return all_data
