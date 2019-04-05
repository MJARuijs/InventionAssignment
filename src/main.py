import argparse
import FileReader
import numpy as np
import Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='File name of the desired data. Use, for example, free_fall_*, to see all free_fall plots', default='free_fall_0*')
parser.add_argument('-s', help='Sensors to be plotted. G=gyroscope, M=Magnetometer, A=accelerometer. GA selects gyro and accelerometer', default='AGM')
parser.add_argument('-p', help='Path to the data.', default='/../res/data/')
args = parser.parse_args()

if __name__ == '__main__':

    # Use the FileReader to read all files at the specified folder, with the specified name
    all_data = FileReader.read_files(args.p, args.f)

    data = []
    delay = 0

    # For each file, append the data to the numpy array,
    # and keep track of the number of measurements, and the delay between measurements
    for file_data in all_data:
        data.append([file_data[2], file_data[3], file_data[4], file_data[5], file_data[1]])
        delay = file_data[0]

    for d in data:
        min_count = d[4]
        time_array = np.linspace(0, min_count * (delay / 1000.0), num=min_count)

        if 'A' in args.s:
            Plotter.plot(time_array, d[0][0:min_count], 'Acceleration ' + d[3])

        if 'G' in args.s:
            Plotter.plot(time_array, d[2][0:min_count], 'Gyroscope ' + d[3])

        if 'M' in args.s:
            Plotter.plot(time_array, d[1][0:min_count], 'Magnetometer ' + d[3])

    Plotter.show()
