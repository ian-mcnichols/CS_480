import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np
import datetime
from itertools import combinations
import math

FINAL_LOCATION = [43.33352346016208, -8.40940731683987]


def distance(a, b):
    # Returns distance between 2 lat/long points in meters
    id1 = a[0]
    id2 = b[0]
    if id1 == id2:
        return 500, 0, 0
    return geodesic(a[1], b[1]).m, id1, id2


def get_user_data(display=False):
    # Goes through the gps .csv and compiles the data into lists of users with times/locations
    user_location_data = {}
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
    # users that are close to each other: 
    for user in users:
        user_times = []
        #good_users = [3, 8, 12, 13]
        #if user not in good_users:
        #    continue
        #else:
        #    print("user:", user)
        # Deciphering timestamp into year/day/hour
        for time in users[user].timestamp:
            datetime_obj = datetime.datetime.fromtimestamp(time)
            month = datetime_obj.month
            day = datetime_obj.day
            hour = datetime_obj.hour
            # minute = datetime_obj.minute
            # second = datetime_obj.second
            user_times.append([month, day, hour])
        # Grab location data about the user
        user_bearings = users[user].gps_bearing
        user_lats = users[user].gps_lat_increment
        user_longs = users[user].gps_long_increment
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
        timed_locations = list(zip(user_times, actual_lats, actual_longs))
        # Add list of times and locations for the specific user to a dictionary of all the suspects
        user_location_data[user] = timed_locations
        # Show the suspect's path if requested
        if display:
            plt.scatter(actual_lats, actual_longs)
            plt.show()
    return user_location_data


def compare_times(users):
    days = []
    for i, user in enumerate(users):
        location = users[user]
        times = np.array([x[0] for x in location])
        for day in times:
            days.append((day[0], day[1], day[2]))
    days_set = set(days)
    return days_set


def location_per_time(timestamps, data):
    # Compiles all the data that is taken at the same year/day/hour
    shared_times = {key : [] for key in timestamps}
    for time in timestamps:
        for user in data:
            for i, timestep in enumerate(data[user]):
                if tuple(timestep[0]) == time:
                    shared_times[time].append([user, data[user][i][1:]])
    return shared_times


def get_distances(locations):
    # Returns all the times there are distances less than 250 between 2 people
    # at the same time
    ids = [location[0] for location in locations]
    if len(set(ids)) == 1:
        return
    else:
        distances = {}
        coordinate_list = [location for location in locations]
        combos = combinations(coordinate_list, 2)
        for combination in combos:
            meters, susa, susb = distance(*combination)
            if meters <= 250 and meters != 500:
                distances[(susa, susb)] = meters
    return distances.copy()


def display_suspects(times_data):
    pairs = []
    for suspicious_time in times_data:
        suspects = times_data[suspicious_time]
        for suspect in suspects:
            pairs.append(suspect)
    print("pairs:", pairs)
    return

if __name__ == "__main__":
    location_data = get_user_data(display=False)
    unique_times = compare_times(location_data)
    important = location_per_time(unique_times, location_data)
    times_data = {}
    for time in important:
        distances_data = get_distances(important[time])
        if distances_data:
            times_data[time] = distances_data
    pairs = []
    for suspicious_time in times_data:
        suspects = times_data[suspicious_time]
        for suspect in suspects:
            pairs.append(suspect)
    print("Displaying data")

    for pair in pairs:
        for user in pairs:
            print("user:", user)
            lats1 = [x[1] for x in location_data[user[0]]]
            longs1 = [x[2] for x in location_data[user[0]]]
            path_data = open("path.txt", "w")
            for i in range(len(lats1)):
                path_data.writelines(str(lats1[i]) + ","+str(longs1[i])+",#ffffff\n")
            path_data.close()
            pause = input("Finished writing data for user:" + str(user[0]))
