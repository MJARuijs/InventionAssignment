import pandas as ps
import json
import os
import glob
import unicodedata
from datetime import datetime


def read_file(path):
    folder = os.getcwd() + path
    absolute_path = glob.glob(folder + '*.json')
    data = []

    device_ids = {
        '247189e98685': 'Remote Control',
        '247189e83001': 'Spider Stick',
        '247189e72603': 'Garden Door',
        '247189e78180': 'Fridge',
        '247189e76106': 'Breakfast Chair',
        '247189e87d85': 'Tray',
        '247189e98d83': 'Chair Pillow',
        '247189ea0782': 'Remote Control',
        '247189e74381': 'Rope on Stairs',
        '247189e64706': 'Kitchen Drawer',
        '247189e61784': 'Fridge',
        '247189e61802': 'Kitchen Chair',
        '247189e61682': 'Fridge',
        '247189e76c05': 'Remote Control',
        '247189e88b80': 'Kitchen Cabinet Door',
        '247189e8e701': 'Knitting Needle',
        '247189e6c680': 'Tablet'
    }

    for f in absolute_path:
        with open(f) as json_data:

            current_data = ps.DataFrame(json.loads(l) for l in json_data)
            timestamps = current_data['timestamp']
            events = current_data['event']
            devices = current_data['deviceId']
            sensor_data = current_data['data']

            for index, _ in enumerate(events):
                current_event = events.values[index]
                current_event = unicodedata.normalize('NFKD', current_event).encode('ascii')

                if current_event == 'accel' or current_event == 'mag' or current_event == 'gyro':
                    current_device = devices.values[index]
                    current_device = unicodedata.normalize('NFKD', current_device).encode('ascii')

                    if current_device in device_ids:
                        current_time = timestamps[index]
                        current_time = unicodedata.normalize('NFKD', current_time).encode('ascii')
                        current_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.%fZ')

                        current_device = device_ids[current_device]
                        current_sensor_data = sensor_data[index]
                        x_data = current_sensor_data['x']
                        y_data = current_sensor_data['y']
                        z_data = current_sensor_data['z']
                        data.append([current_device, current_time.__str__(), current_event, x_data, y_data, z_data])

    for entry in data:
        print(entry)

    return data
