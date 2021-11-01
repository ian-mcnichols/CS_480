import csv
import pandas
from sklearn.linear_model import LinearRegression
import numpy as np


def convert_to_int(activity):
    if activity == "Walking":
        return 1
    elif activity == "Active":
        return 2
    elif activity == "Inactive":
        return 3
    elif activity == "Driving":
        return 4


files = ['data/sensoringData_magn_changed.csv', 'data/sensoringData_gyro_changed.csv',
            'data/sensoringData_acc_changed.csv', 'data/location_data1_changed.csv']
#magn_df = pandas.read_csv(files[0])
#gyro_df = pandas.read_csv(files[1])
#acc_df = pandas.read_csv(files[2])
#loc_df = pandas.read_csv(files[3])
# Load data
merge = pandas.read_csv('data/merged_data.csv')
print("csv's loaded")
# Clean up data
merge = merge.drop(['Unnamed: 0.1'], axis=1)
merge = merge.fillna(-1)
merge['activity'] = np.where(merge['activity'] == "Walking", 1, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Walking", 1, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Active", 2, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Active", 2, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Inactive", 3, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Inactive", 3, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Driving", 4, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Driving", 4, merge['activity'])
# Display data
print(merge)
pause = input("Pausing...")
# Run Linear Regression
regression_model = LinearRegression()
y = merge.activity
regression_model.fit(merge, y)
# Display output
print("Linear regression score:", regression_model.score(merge, y))

#merge.to_csv('data/merged_data.csv')
