import re
import socket
import numpy as np
import FileWriter
import Plotter


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8081

    s.bind(('192.168.178.18', port))
    s.listen(1)

    streaming = False

    delay = 0

    pattern = '([AGM]) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*)'
    file_name = ''

    all_data = np.zeros(0)

    try:
        while True:
            client, address = s.accept()

            message_bytes = client.recv(4)
            size = 0
            size += message_bytes[3] << 24
            size += message_bytes[2] << 16
            size += message_bytes[1] << 8
            size += message_bytes[0]

            bytes_read = 0
            data = b''

            while bytes_read < size - 4:
                data += client.recv(size - bytes_read)
                bytes_read = len(data)

            try:
                decoded_data = data.decode('utf-8')

                if 'START STREAM' in decoded_data:
                    start_index = decoded_data.index('D') + 1
                    delay = decoded_data[start_index: len(decoded_data)]

                    streaming = True
                elif decoded_data == 'STOP STREAM':
                    streaming = False
                else:
                    if streaming:
                        matcher = re.match(pattern, decoded_data, re.M)
                        if matcher:
                            data_type = matcher.group(1)
                            x_value = matcher.group(2)
                            y_value = matcher.group(3)
                            z_value = matcher.group(4)

                            values = [data_type, x_value, y_value, z_value]
                    else:
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

                        for index, string in enumerate(a):
                            if string == '':
                                continue

                            matcher = re.match(pattern, string, re.M)

                            if matcher:
                                data_type = matcher.group(1)
                                x_value = matcher.group(2)
                                y_value = matcher.group(3)
                                z_value = matcher.group(4)

                                values = [x_value, y_value, z_value]
                                if data_type == 'A':
                                    acceleration_data[acceleration_index] = values
                                    acceleration_index += 1
                                elif data_type == 'G':
                                    gyroscope_data[gyroscope_index] = values
                                    gyroscope_index += 1
                                elif data_type == 'M':
                                    magnetometer_data[magnetometer_index] = values
                                    magnetometer_index += 1
                            elif string[0] == 'D':
                                delay = int(string[1:])
                            elif string[0] == 'N':
                                file_name = string[1:]

                        counts = []

                        if acceleration_count is not 0:
                            counts.append(acceleration_count)

                        if magnetometer_count is not 0:
                            counts.append(magnetometer_count)

                        if gyroscope_count is not 0:
                            counts.append(gyroscope_count)

                        min_count = 0
                        if len(counts) is not 0:
                            min_count = min(counts)

                        acceleration_data = acceleration_data[0:min_count]
                        magnetometer_data = magnetometer_data[0:min_count]
                        gyroscope_data = gyroscope_data[0:min_count]

                        time_array = np.linspace(0, min_count * (delay / 1000), num=min_count)

                        if file_name is not '':
                            file_data = ''
                            file_data += 'D%d\n' % int(delay)
                            file_data += '~A%d\n' % min_count
                            for i in acceleration_data:
                                file_data += '%.4f %.4f %.4f\n' % (i[0], i[1], i[2])
                            file_data += '~M%d\n' % min_count

                            for i in magnetometer_data:
                                file_data += '%.4f %.4f %.4f\n' % (i[0], i[1], i[2])

                            file_data += '~G%d\n' % min_count
                            for i in gyroscope_data:
                                file_data += '%.4f %.4f %.4f\n' % (i[0], i[1], i[2])

                            FileWriter.write_to_file('../res/data/', file_name, file_data)

                        if acceleration_count is not 0:
                            Plotter.plot(time_array, acceleration_data, 'Acceleration')

                        if magnetometer_count is not 0:
                            Plotter.plot(time_array, magnetometer_data, 'Magnetometer')

                        if gyroscope_count is not 0:
                            Plotter.plot(time_array, gyroscope_data, 'Gyroscope')

            except UnicodeDecodeError:
                print('Unicode error..')

            client.close()
    except KeyboardInterrupt:
        s.close()


# def match_string():
#     matcher = re.match(pattern, string, re.M)
#
#     if matcher:
#         data_type = matcher.group(1)
#         x_value = matcher.group(2)
#         y_value = matcher.group(3)
#         z_value = matcher.group(4)
#         return [data_type, x_value, y_value, z_value]

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
