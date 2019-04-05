import argparse
import re
import socket
import numpy as np
import FileWriter
import Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-p', help='Port of the server', default=8081)
args = parser.parse_args()

if __name__ == '__main__':
    port = int(args.p)

    # Ping Google's servers in order to find our IP address
    ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_socket.connect(('8.8.8.8', 10002))
    address = ip_socket.getsockname()[0]
    ip_socket.close()

    print('Address is: %s' % address)

    # Initialize server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(1)

    delay = 0

    # Create regex pattern which can be used to parse data sent by the phone
    pattern = '([AGM]) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*) (-?[0-9]*.[0-9]*)'
    file_name = ''

    all_data = np.zeros(0)

    try:
        while True:

            # Accept a client and receive the size of the data
            client, address = s.accept()
            message_bytes = bytearray(4)
            client.recv_into(message_bytes, 4)

            size = 0
            size += message_bytes[3] << 24
            size += message_bytes[2] << 16
            size += message_bytes[1] << 8
            size += message_bytes[0]

            bytes_read = 0
            data = b''

            # Receive all the data from the client
            while bytes_read < size - 4:
                data += client.recv(size - bytes_read)
                bytes_read = len(data)

            try:
                # Decode the data, and split it into the different sensors
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

                for index, string in enumerate(a):
                    if string == '':
                        continue

                    # Use the regex pattern to easily parse the sensor data
                    matcher = re.match(pattern, string, re.M)

                    if matcher:
                        data_type = matcher.group(1)
                        x_value = matcher.group(2)
                        y_value = matcher.group(3)
                        z_value = matcher.group(4)

                        # Add the sensor values to their corresponding numpy arrays
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
                        # Fetch the delay between measurements, as specified in the Android app. Usually 10ms
                        delay = int(string[1:])
                    elif string[0] == 'N':
                        # Fetch the file name specified in the Android app
                        file_name = string[1:]

                counts = []

                # Create an array containing the amount of measurements of each of the sensors.
                if acceleration_count is not 0:
                    counts.append(acceleration_count)

                if magnetometer_count is not 0:
                    counts.append(magnetometer_count)

                if gyroscope_count is not 0:
                    counts.append(gyroscope_count)

                # Compute the minimum number of measurements
                min_count = 0
                if len(counts) is not 0:
                    min_count = min(counts)

                # Trim all sensor measurements to be the same size as the minimum number of measurements
                acceleration_data = acceleration_data[0:min_count]
                magnetometer_data = magnetometer_data[0:min_count]
                gyroscope_data = gyroscope_data[0:min_count]

                time_array = np.linspace(0, min_count * (delay / 1000.0), num=min_count)

                # Write the data to a file
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

                # Plot the data, assuming it exists
                if acceleration_count is not 0:
                    Plotter.plot_triple(time_array, acceleration_data, 'Acceleration')

                if magnetometer_count is not 0:
                    Plotter.plot_triple(time_array, magnetometer_data, 'Magnetometer')

                if gyroscope_count is not 0:
                    Plotter.plot_triple(time_array, gyroscope_data, 'Gyroscope')

                Plotter.show()

            except UnicodeDecodeError:
                print('Unicode error..')

            # Close the client
            client.close()

    except KeyboardInterrupt:

        # Close the server
        s.close()
