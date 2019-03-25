# -*- coding: utf-8 -*-
# @Author: yanxia
# @Date:   2017-03-30 16:23:44
# @Last Modified by:   yanxia
# @Last Modified time: 2017-10-16 09:08:08

import datetime
import matplotlib
import preprocess

matplotlib.style.use('ggplot')


# import cluster

sensors = ['accelx', 'accely', 'accelz',
           'magx', 'magy', 'magz',
           'gyrox', 'gyroy', 'gyroz',
           'rssi_air', 'pressure_air', 'humidity_air',
           'temperature_air', 'lux_air', 'battery_air']

objects01 = {'247189e98685': 'Remote Control',
             '247189e83001': 'Spider Stick',
             '247189e72603': 'Garden Door',
             '247189e78180': 'Fridge',
             '247189e76106': 'Breakfast Chair',
             '247189e87d85': 'Tray',
             }

objects02 = {'247189e98d83': 'Chair Pillow',
             '247189ea0782': 'Remote Control',
             '247189e74381': 'Rope on Stairs',
             '247189e64706': 'Kitchen Drawer',
             '247189e61784': 'Fridge'
             }

objects03 = {'247189e61802': 'Kitchen Chair',
             '247189e61682': 'Fridge',
             '247189e76c05': 'Remote Control',
             '247189e88b80': 'Kitchen Cabinet Door',
             '247189e8e701': 'Knitting Needle',
             '247189e6c680': 'Tablet'
             }

objIndex = 2
objects = [objects01, objects02, objects03][objIndex]


def main():
    data_dir = '/../../res/data/'  # '/data/'
    file_name = "*.json"
    # file_name = "*07-*"  # "*2017-04-05.txt"
    num_home = 2  # Use everything is 'ALL'; otherwise integer
    num_device = objects  # 'ALL'  # Use everything is 'ALL'; otherwise integer
    num_modality = [3,4,5]  # 'ALL'  # Use everything is 'ALL'; otherwise integer
    show_plot = True
    is_normalized = True
    start_date = datetime.date(2017, 7, 1)
    end_date = datetime.date(2017, 9, 29)

    alldata = {}
    alldata, per_device = preprocess.convert_to_DataFrame_TI(data_dir, file_name, num_home, num_device, num_modality,
                                                             show_plot, start_date, end_date)


if __name__ == "__main__":
    main()
