import argparse
import FileReader
import numpy as np
import Plotter
import Model

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='File name of the desired data. Use, for example, free_fall_*, to see all free_fall plots', default='free_fall_0*')
parser.add_argument('-s', help='Sensors to be plotted. G=gyroscope, M=Magnetometer, A=accelerometer. GA selects gyro and accelerometer', default='AGM')
parser.add_argument('-p', help='Path to the data.', default='/../res/data/training_set/')
args = parser.parse_args()

if __name__ == '__main__':

    # Use the FileReader to read all files at the specified folder, with the specified name
    all_data = FileReader.read_files(args.p, args.f)

    data = []
    delay = 0

    # For each file, append the data to the numpy array,
    # and keep track of the number of measurements, and the delay between measurements
    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000.0), num=file_data[1])
        data.append([file_data[2], file_data[3], file_data[4], file_data[5], time_array])

    for d in data:
        scores = Model.process(d, 5, len(d[0]))
        Plotter.plot_single(d[4], scores, 'scores ' + d[3])

        if 'A' in args.s:
            Plotter.plot_triple(d[4], d[0], 'Acceleration ' + d[3])

        if 'G' in args.s:
            Plotter.plot_triple(d[4], d[2], 'Gyroscope ' + d[3])

        if 'M' in args.s:
            Plotter.plot_triple(d[4], d[1], 'Magnetometer ' + d[3])

        Plotter.show()
