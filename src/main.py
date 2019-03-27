import data_reader
import pylab as pl

if __name__ == '__main__':
    data_dir = '/../res/data/'
    data = data_reader.read_file(data_dir)

    devices = {}

    for measurement in data:
        device_name = measurement[0]
        measurement_type = measurement[2]

        if device_name not in devices:
            devices[device_name] = {}
            devices[device_name][measurement_type] = [measurement[1], measurement[3:]]
        elif measurement_type not in devices[device_name]:
            devices[device_name][measurement_type] = [measurement[1], measurement[3:]]
        else:
            devices[device_name][measurement_type].append([measurement[1], measurement[3:]])

    for device_name, measurements in devices.items():
        print(device_name)

        for measurement_name, measurement in measurements.items():
            print(measurement_name)
            print(measurement)
            print()
        print()

