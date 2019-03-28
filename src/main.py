import pylab as pl
import re
import socket
import numpy as np

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8081

    s.bind(('192.168.178.18', port))
    s.listen(1)

    try:
        while True:
            client, address = s.accept()

            message_bytes = client.recv(4)
            size = 0
            size += message_bytes[3] << 24
            size += message_bytes[2] << 16
            size += message_bytes[1] << 8
            size += message_bytes[0]

            data = client.recv(size)

            try:
                decoded_data = data.decode('utf-8')
                a = decoded_data.split('!')

                acceleration_count = decoded_data.count('A')
                gyroscope_count = decoded_data.count('G')
                magnetometer_count = decoded_data.count('M')

                acceleration_data = np.zeros(3 * acceleration_count).reshape([acceleration_count, 3])
                gyroscope_data = np.zeros(3 * gyroscope_count).reshape([gyroscope_count, 3])
                magnetometer_data = np.zeros(3 * magnetometer_count).reshape([magnetometer_count, 3])

                acceleration_index = 0
                gyroscope_index = 0
                magnetometer_index = 0

                delay = 0

                for index, string in enumerate(a):
                    matcher = re.match('([AGM]) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*)', string, re.M)

                    if matcher:
                        data_type = matcher.group(1)
                        x_value = matcher.group(2)
                        y_value = matcher.group(3)
                        z_value = matcher.group(4)

                        if data_type == 'A':
                            acceleration_data[acceleration_index] = [x_value, y_value, z_value]
                            acceleration_index += 1
                        elif data_type == 'G':
                            gyroscope_data[gyroscope_index] = [x_value, y_value, z_value]
                            gyroscope_index += 1
                        elif data_type == 'M':
                            magnetometer_data[magnetometer_index] = [x_value, y_value, z_value]
                            magnetometer_index += 1
                    elif string[0] == 'D':
                        delay = int(string[1:])

                acc_time_array = np.zeros(acceleration_count)
                for i in range(0, acceleration_count):
                    acc_time_array[i] = i * delay

                mag_time_array = np.zeros(magnetometer_count)
                for i in range(0, acceleration_count):
                    mag_time_array[i] = i * delay

                gyro_time_array = np.zeros(gyroscope_count)
                for i in range(0, acceleration_count):
                    gyro_time_array[i] = i * delay

                acc_figure, acc_axis = pl.subplots()
                acc_axis.set_title('Acceleration')
                acc_axis.plot(acc_time_array, acceleration_data[:, 0], label='X')
                acc_axis.plot(acc_time_array, acceleration_data[:, 1], label='Y')
                acc_axis.plot(acc_time_array, acceleration_data[:, 2], label='Z')
                acc_axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
                acc_figure.show()

                mag_figure, mag_axis = pl.subplots()
                mag_axis.set_title('Magnetometer')
                mag_axis.plot(mag_time_array, magnetometer_data[:, 0], label='X')
                mag_axis.plot(mag_time_array, magnetometer_data[:, 1], label='Y')
                mag_axis.plot(mag_time_array, magnetometer_data[:, 2], label='Z')
                mag_axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
                mag_figure.show()

                gyro_figure, gyro_axis = pl.subplots()
                gyro_axis.set_title('Gyroscope')
                gyro_axis.plot(gyro_time_array, gyroscope_data[:, 0], label='X')
                gyro_axis.plot(gyro_time_array, gyroscope_data[:, 1], label='Y')
                gyro_axis.plot(gyro_time_array, gyroscope_data[:, 2], label='Z')
                gyro_axis.legend(loc=5, bbox_to_anchor=(1.15, 0.92))
                gyro_figure.show()

            except UnicodeDecodeError:
                print('Unicode error..')

            client.close()
    except KeyboardInterrupt:
        s.close()

    # data_dir = '/../res/data/'
    # data = data_reader.read_file(data_dir)
    #
    # devices = {}
    #
    # for measurement in data:
    #     device_name = measurement[0]
    #     measurement_type = measurement[2]
    #
    #     if device_name not in devices:
    #         devices[device_name] = {}
    #         devices[device_name][measurement_type] = [measurement[1], measurement[3:]]
    #     elif measurement_type not in devices[device_name]:
    #         devices[device_name][measurement_type] = [measurement[1], measurement[3:]]
    #     else:
    #         devices[device_name][measurement_type].append([measurement[1], measurement[3:]])
    #
    # for device_name, measurements in devices.items():
    #     print(device_name)
    #
    #     for measurement_name, measurement in measurements.items():
    #         print(measurement_name)
    #         print(measurement)
    #         print()
    #     print()
