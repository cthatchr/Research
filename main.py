from geopy import distance
from Algorithm import *
from Station import *
from User import *
from DistList import *
import numpy as np
import matplotlib.pyplot as plt
import citybikes
import pandas as pd
import json
from pandas.io.json import json_normalize
from datetime import datetime

def startup():
    choice = {}
    choice['1'] = "Random Data"
    choice['2'] = "Real Data"

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':
            set_rand_settings()
            break
        elif selection == '2':
            set_real_settings()
            break
        else:
            print('select again')

def set_real_settings(): # select settings for real data run
    settings = []

    while True:
        try:
            settings.append((int(input
                                 ('A random date will be used. In minutes, how many user trips would you like to use?:'))))
            break
        except:
            print('Enter an integer.')

    run_real(settings)

def set_rand_settings():
    settings = []
    choice = {}
    choice['1'] = "Default Priority (Difference/Distance)"
    choice['2'] = "Distance Priority (Difference/Distance\u00b2)"

    # select settings
    while True:
        try:
            settings.append((int(input('How many stations would you like to create?:'))))
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('How many incoming users would you like to create?:')))
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('How many incoming users are we allowed to move?:')))
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('Number of tests per run?:')))
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':
            settings.append(1)
            break
        elif selection == '2':
            settings.append(2)
            break
        else:
            print('select again')

    run_random(settings)


def run_random(settings): # runs with same random data
    stats_sum = []
    stats_avg = []
    stats_dist = []
    index = np.arange(settings[2]+1)
    j_sum = []
    j_avg = []
    j_dist = []

    targ = Station(lat=40.7127, lon=-74.0059)  # target is NYC

    for j in range(settings[3]):  # run algorithm j times, i.e 50

        stations = create_rand_stations(targ.lat, targ.lon, 2000, settings[0])  # create stations
        users = create_rand_users(stations, settings[1])  # create users

        kth_sum = []
        kth_avg = []
        kth_dist = []

        for k in range(settings[2] + 1):  # run with same settings, k times, i.e users moved

            if k == 0:  # run distribution 0 times if moving 0 users, else run distribution. then record data
                distribute_incr(stations, settings[4], 0)  # runs algorithm, rerouting a single user then recording data
            else:
                distribute_incr(stations, settings[4])  # runs algorithm, rerouting a single user then recording data

            sum = StationsDiff(stations)  # get sum of stations difference in stock before, per run
            dist_rr = total_RR_distance(users) # get the total distance users were rerouted
            avg = sum / len(stations)  # avg difference, per run

            kth_sum.append(sum)
            kth_avg.append(avg)
            kth_dist.append(dist_rr)

        j_sum = np.array(kth_sum)
        j_avg = np.array(kth_avg)
        j_dist = np.array(kth_dist)

        if j == 0: # initialize np array if first run, then start adding
            stats_sum = j_sum
            stats_avg = j_avg
            stats_dist = j_dist
        else:
            stats_sum = np.add(stats_sum, j_sum)
            stats_avg = np.add(stats_avg, j_avg)
            stats_dist = np.add(stats_dist, j_dist)

    stats_sum = np.divide(stats_sum, settings[3])
    stats_avg = np.divide(stats_avg, settings[3])
    stats_dist = np.divide(stats_dist, settings[3])

    print(index, stats_sum, stats_avg, stats_dist)
    create_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here


def run_real(settings): # runs with real dataset

    stations = load_stations()
    users = load_users(stations, settings[0])

    stats_sum = []
    stats_avg = []
    stats_dist = []
    index = np.arange(len(users)+1)

    for k in range(len(users)+1):  # run with real data

        if k > 0:  # run distribution 0 if not moving user
            distribute_incr(stations)  # runs algorithm, rerouting a single user then recording data

        sum = StationsDiff(stations)  # get sum of stations difference in stock before, per run
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    stats_sum = np.array(stats_sum)
    stats_avg = np.array(stats_avg)
    stats_dist = np.array(stats_dist)
    # print(index, stats_sum, stats_avg, stats_dist)
    create_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here




def create_lineplot(index, sum, avg, dist):
    # create a line plot given a set of data
    plt.figure()
    plt.suptitle('Stock Difference After Algorithm', fontsize=16)
    plt.subplots_adjust(hspace=1)
    # plot sums
    plt.subplot(211)
    plt.title('Total')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, sum)
    plt.locator_params(axis='y', nbins=5)
    # plot avgs
    plt.subplot(212)
    plt.title('Average')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, avg)
    plt.locator_params(axis='y', nbins=5)

    plt.figure()
    # user distance moved
    # plt.subplot(313)
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Meters)')
    plt.plot(index, dist)
    plt.locator_params(axis='y', nbins=5)
    plt.show()


def test():
    pd.set_option('display.max_columns', None)

    df = pd.read_csv('indego-trips-2019-q1.csv')

    load_users([],10)



run_real([50])

