import FileReader
import numpy as np
import Plotter
import model


if __name__ == '__main__':

    # Use the FileReader to read all files at the specified folder, with the specified name
    all_data = FileReader.read_files('/../res/data/test_set/', 'free_*.txt')

    data = []
    delay = 0

    # For each file, append the data to the numpy array,
    # and keep track of the number of measurements, and the delay between measurements
    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000.0), num=file_data[1])
        data.append([file_data[2], file_data[3], file_data[4], file_data[5], time_array])


    for d in data:
        Plotter.plot_triple(d[4], d[0], 'Acceleration ' + d[3])
        Plotter.plot_triple(d[4], d[1], 'Magnetometer ' + d[3])
        Plotter.plot_triple(d[4], d[2], 'Gyroscope ' + d[3])

        scores = model.process(d, 5, len(d[0]))
        Plotter.plot_single(d[4], scores, 'scores ' + d[3])

