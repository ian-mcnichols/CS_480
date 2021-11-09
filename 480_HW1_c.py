import csv
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA


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
merge = merge.drop(["activity_id"], axis=1)
try:
    merge = merge.drop(['Unnamed: 0.1'], axis=1)
except KeyError:
    pass
try:
    merge = merge.drop(['Unnamed: 0'], axis=1)
except KeyError:
    pass
merge = merge.fillna(-1)
# Turn activity types to int ID's
merge['activity'] = np.where(merge['activity'] == "Walking", 1, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Walking", 1, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Active", 2, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Active", 2, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Inactive", 3, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Inactive", 3, merge['activity'])
merge['activity'] = np.where(merge['activity'] == " Driving", 4, merge['activity'])
merge['activity'] = np.where(merge['activity'] == "Driving", 4, merge['activity'])
# Load keys
y = merge.activity
y = [x for x in y]
merge = merge.drop(['activity'], axis=1)
# Dimensionality reduction
pca = PCA(n_components=5)
merge = pca.fit_transform(merge)
# Use random forest regressor
model = RandomForestRegressor(max_samples=.5,n_jobs=24, verbose=2)
clf = make_pipeline(StandardScaler(), model)
clf.fit(merge, y)
#disp = plot_confusion_matrix(model, X, data_types, cmap=plt.cm.Blues)
#plt.show()
print("random forest regressor score:", clf.score(merge, y))
# Results = Linear regression score: 0.01642565849091837
# with: timestamp  magn_x_axis  magn_y_axis  magn_z_axis  gyro_x_axis  gyro_y_axis  gyro_z_axis  acc_x_axis  acc_y_axis  acc_z_axis  lat  long > activity type
#merge.to_csv('data/merged_data.csv')
