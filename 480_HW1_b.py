"""
2. For each suspect, analyze the GPS trajectories taking into account the
time with the aim to see if there is any correlation between the activities
and the reported GPS coordinates (you are really trying to see if you can
estimate the activity by looking at the GPS coordinates). [15 Points]
"""
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
from geopy.distance import geodesic
from sklearn.svm import SVC
from sklearn.svm import SVR
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import scipy
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import plot_confusion_matrix, ConfusionMatrixDisplay

FINAL_LOCATION = [43.33352346016208, -8.40940731683987]


def write_data_file(display=False):
    csv_file = open("data/location_data.csv", "w")
    csv_file.writelines("activity,time,lat,long,activity_id\n")
    # Goes through the gps .csv and compiles the data into lists of users with times/locations
    users = {}
    usernames = []
    sensoring_gps = pd.read_csv("data/sensoringData_gps.csv")
    # grabbing all unique user id's
    for username in sensoring_gps.username:
        usernames.append(username)
    usernames = list(set(usernames))
    # Sorting data into a dictionary, with 1 entry per suspect
    for i in usernames:
        users[i] = sensoring_gps.loc[sensoring_gps['username'] == i]
    # Performing calculations on each suspect to get location data
    for user in users:
        user_times = []
        # Deciphering timestamp into year/day/hour
        for time in users[user].timestamp:
            datetime_obj = datetime.datetime.fromtimestamp(time)
            month = datetime_obj.month
            day = datetime_obj.day
            hour = datetime_obj.hour
            # minute = datetime_obj.minute
            # second = datetime_obj.second
            user_times.append([month, day, hour])
        user_times = users[user].timestamp
        # Grab location data about the user
        user_bearings = users[user].gps_bearing
        user_lats = users[user].gps_lat_increment
        user_longs = users[user].gps_long_increment
        # Grab activity
        activity_ids = users[user].activity_id
        user_activities = users[user].activity
        ids = users[user].id
        # Initialize location data with pickup point
        actual_longs = [FINAL_LOCATION[1]]
        actual_lats = [FINAL_LOCATION[0]]
        # Turn data into python list
        longitudes = [longitude for longitude in user_longs]
        latitudes = [latitude for latitude in user_lats]
        bearings = [bearing for bearing in user_bearings]
        # Work backwards from pickup point by subtracting change in lat/long
        for i, longitude in enumerate(longitudes[::-1]):
            delta_long = math.sin(bearings[i])*longitude
            actual_longs.append(actual_longs[-1] - delta_long)
        for i, latitude in enumerate(latitudes[::-1]):
            delta_lat = math.cos(bearings[i])*latitude
            actual_lats.append(actual_lats[-1] - delta_lat)
        # Reverse so data starts at first location instead of pickup point
        actual_longs = actual_longs[1:][::-1]
        actual_lats = actual_lats[1:][::-1]
        timed_locations = list(zip(user_times, user_activities, actual_lats, actual_longs, activity_ids, ids))
        # Add list of times and locations for the specific user to a dictionary of all the suspects
        for datapoint in timed_locations:
            lat = datapoint[2]
            long = datapoint[3]
            time = datapoint[1]
            csv_file.writelines(str(datapoint[5]) + ", "+ str(datapoint[1]) + ", " + str(datapoint[0]) + ", " +
                                str(datapoint[2]) + ", " + str(datapoint[3]) +
                                ", " + str(datapoint[4]) + "\n")
    csv_file.close()


def read_data_file():
    data = pd.read_csv("location_data.csv")
    data_types = data.activity
    data_types = [x for x in data_types]
    data_types = convert_to_int(data_types)
    return data.lat, data.long, data.time, data_types


def convert_to_int(data):
    for i in range(len(data)):
        if data[i] == 'Driving' or data[i] == ' Driving':
            data[i] = 1
        elif data[i] == 'Walking' or data[i] == ' Walking':
            data[i] = 2
        elif data[i] == 'Inactive' or data[i] == ' Inactive':
            data[i] = 3
        elif data[i] == 'Active' or data[i] == ' Active':
            data[i] = 4
    return data


def calculate_correlation(lat, long, time, data_types):
    data_types = convert_to_int(data_types)
    #clf = make_pipeline(StandardScaler(), SVC(gamma='auto', kernel='rbf'))
    lat = [x for x in lat]
    long = [x for x in long]
    time = [x for x in time]
    X = np.array([lat, long, time])
    X = np.reshape(X, (19079, 3))
    #clf.fit(X, data_types)
    #print("SVM:", clf.score(X, data_types))
    '''
    svr_rbf = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
    svr_lin = SVR(kernel="linear", C=100, gamma="auto")
    svr_poly = SVR(kernel="poly", C=100, gamma="auto", degree=3, epsilon=0.1, coef0=1)
    svrs = [svr_rbf, svr_lin, svr_poly]
    kernel_label = ["RBF", "Linear", "Polynomial"]
    model_color = ["m", "c", "g"]
    lw = 2

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 10), sharey=True)
    for ix, svr in enumerate(svrs):
        axes[ix].plot(
            X,
            svr.fit(X, data_types).predict(X),
            color=model_color[ix],
            lw=lw,
            label="{} model".format(kernel_label[ix]),
        )
        print("Finished predicting model")
    plt.show()
    '''
    # Use random forest regressor
    model = RandomForestRegressor(max_features=3)
    model.fit(X, data_types)
    #disp = plot_confusion_matrix(model, X, data_types, cmap=plt.cm.Blues)
    #plt.show()
    print("random forest regressor score:", model.score(X, data_types))




if __name__ == "__main__":
    #write_data_file()
    lats, longs, times, data_types = read_data_file()
    calculate_correlation(lats, longs, times, data_types)
