import FileReader
import numpy as np
import Plotter
import model


if __name__ == '__main__':
    all_data = FileReader.read_files('/../res/data/', 'throw_6.txt')

    min_counts = []
    data = []
    delay = 0

    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000), num=file_data[1])
        min_counts.append(file_data[1])
        data.append([file_data[2], file_data[3], file_data[4], file_data[5]])
        delay = file_data[0]

    min_count = min(min_counts)

    time_array = np.linspace(0, min_count * (delay / 1000.0), num=min_count)

    for d in data:
        Plotter.plot_triple(time_array, d[0][0:min_count], 'Acceleration ' + d[3])
        Plotter.plot_triple(time_array, d[1][0:min_count], 'Magnetometer ' + d[3])
        Plotter.plot_triple(time_array, d[2][0:min_count], 'Gyroscope ' + d[3])

        scores = model.process(d, 5, min_count)
        Plotter.plot_single(time_array,scores, 'scores')
