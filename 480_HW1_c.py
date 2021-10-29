import csv
import pandas


def write_data_file(display=False):
    files = ['data/sensoringData_magn_changed.csv', 'data/sensoringData_gyro_changed.csv',
             'data/sensoringData_acc_changed.csv', 'data/location_data1_changed.csv']
    magn_df = pandas.read_csv(files[0])
    gyro_df = pandas.read_csv(files[1])
    acc_df = pandas.read_csv(files[2])
    loc_df = pandas.read_csv(files[3])
    print("csv's loaded")
    magn_gyro_merge = pandas.concat([magn_df, gyro_df, acc_df, loc_df])
    print(magn_gyro_merge)


write_data_file(display=False)
