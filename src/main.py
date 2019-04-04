import FileReader
import numpy as np
import Plotter
import model


if __name__ == '__main__':
    all_data = FileReader.read_files('/../res/data/training_set/', 'throw_*.txt')

    min_counts = []
    data = []
    delay = 0

    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000.0), num=file_data[1])
        min_counts.append(file_data[1])
        data.append([file_data[2], file_data[3], file_data[4], file_data[5], time_array])
        delay = file_data[0]

    min_count = min(min_counts)

    time_array = np.linspace(0, min_count * (delay / 1000.0), num=min_count)

    for d in data:
        Plotter.plot_triple(d[4], d[0], 'Acceleration ' + d[3])
        # Plotter.plot_triple(d[4], d[1], 'Magnetometer ' + d[3])
        Plotter.plot_triple(d[4], d[2], 'Gyroscope ' + d[3])

        scores = model.process(d, 20, len(d[0]))
        Plotter.plot_single(d[4], scores, 'scores ' + d[3])
