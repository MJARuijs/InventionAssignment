import FileReader
import numpy as np
import Plotter


if __name__ == '__main__':
    all_data = FileReader.read_files('/../res/data/', 'free*.txt')
    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000), num=file_data[1])
        Plotter.plot(time_array, file_data[2], 'Acceleration ' + file_data[5])
        Plotter.plot(time_array, file_data[3], 'Magnetometer ' + file_data[5])
        Plotter.plot(time_array, file_data[4], 'Gyroscope ' + file_data[5])
