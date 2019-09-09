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
import copy
import folium as fl

def startup():
    choice = {}
    choice['1'] = "Random Data"
    choice['2'] = "Real Data"
    choice['3'] = "Current Testing"

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
        elif selection == '3':
            curr_settings()
            break
        else:
            print('select again')

def set_real_settings(): # select settings for real data run
    settings = []
    choice = {}
    choice['1'] = "Low"
    choice['2'] = "Medium"
    choice['3'] = "High"
    choice['4'] = "Random"

    while True:
        try:
            settings.append((int(input
                                 ('A random date will be used. In minutes, how many user trips would you like to use?:'))))
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Target Distribution:"))
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    stations = load_stations()  # loads stations with specific target distribution
    set_stations_t_distr(stations, settings[1])  # sets target distribution for stations
    users = load_users_time(stations, settings[0])

    compare_real(stations, users)
    # run_real(settings)

def set_rand_settings():
    settings = []
    choice = {}
    choice['1'] = "Low"
    choice['2'] = "Medium"
    choice['3'] = "High"
    choice['4'] = "Random"

    # select settings
    """while True:
        try:
            settings.append((int(input('How many stations would you like to create?:'))))  # 0
            break
        except:
            print('Enter an integer.')"""

    settings.append(1)
    while True:
        try:
            settings.append(int(input('How many incoming users would you like to create?:')))  # 1
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('How many incoming users are we allowed to move?:')))  # 2
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('Number of tests per run?:')))  # 3
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Target Distribution:"))  # 4
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Current Distribution:"))  # 5
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    stations = load_stations()  # create an instance of stations with curr/target amt
    compare_random(stations, settings)


def run_random(stations, users, settings, p):  # runs with same random data

    sum = StationsDiff(stations)  # get sum of stations difference in stock before run
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    avg = sum / len(stations)  # avg difference rerouted

    stats_sum = [sum]
    stats_avg = [avg]
    stats_dist = [dist_rr]

    for k in range(settings[2]):  # users allowed to move

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            distribute(stations, p)  # runs algorithm, rerouting a single user then recording data
        else:
            print('stations MEET targets')

        sum = StationsDiff(stations)  # get sum of stations difference in stock before, per run
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_sum, stats_avg, stats_dist]  # return instance j's stats for priority x


def run_real(stations, users,  p):  # runs with real dataset

    sum = StationsDiff(stations)  # get sum of stations difference in stock before run
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    avg = sum / len(stations)  # avg difference, per run

    stats_sum = [sum]
    stats_avg = [avg]
    stats_dist = [dist_rr]

    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            distribute(stations, p)  # runs algorithm, rerouting a single user then recording data
        else:
            print('stations MEET targets')

        sum = StationsDiff(stations)  # get sum of stations difference in stock
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_sum, stats_avg, stats_dist]


def compare_random(stations, settings):
    stats_sum = np.array([[0]*(settings[1]+1)]*6)  # initialize stat arrays
    stats_avg = np.array([[0]*(settings[1]+1)]*6)
    stats_dist = np.array([[0]*(settings[1]+1)]*6)
    index = np.arange(settings[1]+1)

    for j in range(settings[3]):  # run algorithm j times, i.e 50
        set_stations_t_distr(stations, settings[4])  # reset the target distribution
        set_stations_c_distr(stations, settings[5])  # reset the current distribution
        delete_inc(stations)  # clear users from stations
        users = create_rand_users(stations, settings[1])  # create random incoming users to stations

        for x in range(6):  # runs algorithm with different priority, starts fresh each time
            reset_users(users)  # reset users back to original positions
            stats = run_random(stations, users, settings, x)  # run alg and gather data for priority x

            stats_sum[x] = np.add(stats_sum[x], stats[0])  # record instance data
            stats_avg[x] = np.add(stats_avg[x], stats[1])
            stats_dist[x] = np.add(stats_dist[x], stats[2])

    delete_inc(stations)  # clear users from stations

    stats_sum = stats_sum / settings[3]
    stats_avg = stats_avg / settings[3]
    stats_dist = stats_dist / settings[3]

    compare_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here


def compare_real(stations, users):  # runs and compares real data against the different priority options
    stats_sum = []
    stats_avg = []
    stats_dist = []
    index = np.arange(len(users)+1)

    for x in range(6):  # runs algorithm with different prio, starts fresh each time
        stats = run_real(stations, users, x)  # run alg and gather data for priority x
        stats_sum.append(stats[0])  # fill data into arrays to use to create plots
        stats_avg.append(stats[1])
        stats_dist.append(stats[2])
        reset_users(users)  # reset users back to original positions

    stats_sum = np.array(stats_sum)
    stats_avg = np.array(stats_avg)
    stats_dist = np.array(stats_dist)

    # print(stats_dist)
    compare_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here


def compare_lineplot(index, sum, avg, dist):
    # create a line plot given a set of data
    plt.figure()
    plt.suptitle('Stock Difference After Algorithm', fontsize=16)
    plt.subplots_adjust(hspace=1)
    # plot sums
    plt.subplot(211)
    plt.title('Total')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, sum[0], label='Default')
    plt.plot(index, sum[1], label='Distance^2')
    plt.plot(index, sum[2], label='Difference^2')
    plt.plot(index, sum[3], label='Only Distance')
    plt.plot(index, sum[4], label='Only Difference')
    plt.plot(index, sum[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    # plot avgs
    plt.subplot(212)
    plt.title('Average')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, avg[0], label='Default')
    plt.plot(index, avg[1], label='Distance^2')
    plt.plot(index, avg[2], label='Difference^2')
    plt.plot(index, avg[3], label='Only Distance')
    plt.plot(index, avg[4], label='Only Difference')
    plt.plot(index, avg[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.figure()

    # user distance moved
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Meters)')
    plt.plot(index, dist[0], label='Default')
    plt.plot(index, dist[1], label='Distance^2')
    plt.plot(index, dist[2], label='Difference^2')
    plt.plot(index, dist[3], label='Only Distance')
    plt.plot(index, dist[4], label='Only Difference')
    plt.plot(index, dist[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.show()


def create_dist_plot(index, dist):
    # user distance moved
    plt.figure()
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Meters)')
    plt.plot(index, dist[0], label='Default')
    plt.plot(index, dist[1], label='Distance^2')
    plt.plot(index, dist[2], label='Difference^2')
    plt.plot(index, dist[3], label='Only Distance')
    plt.plot(index, dist[4], label='Only Difference')
    plt.plot(index, dist[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.show(block=False)


def curr_settings():  # current build for testing purposes
    t = (39.953555, -75.164042)
    settings = []
    choice = {}
    choice['1'] = "Distance Constraint"
    choice['2'] = "No Distance Constraint"
    choice['3'] = "Compare"


    while True:
        try:
            settings.append((int(input('How many users would you like to create and reroute?:'))))
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':  # with a distance constraint
            settings.append((int(input('Distance?:'))))
            stations = load_stations()  # loads stations, their target = curr
            # filter_stations(stations, 1000, t)  # filters out farther stations
            variance = create_sd_dist(settings[0],
                                      stations)  # figure out stations target(i.e. their surplus and deficit)
            users = dist_users(variance, stations)
            compare_curr(stations, users, settings[1])
            break
        elif selection == '2':  # no distance constraint
            settings.append(None)
            stations = load_stations()  # loads stations, their target = curr
            # filter_stations(stations, 1000, t)  # filters out farther stations
            variance = create_sd_dist(settings[0],
                                      stations)  # figure out stations target(i.e. their surplus and deficit)
            users = dist_users(variance, stations)
            compare_curr(stations, users, settings[1])
            break
        elif selection == '3': # compare run with and without a distance constraint
            settings.append((int(input('Distance?:'))))

            stations = load_stations()  # loads stations, their target = curr
            # filter_stations(stations, 1000, t)  # filters out farther stations
            variance = create_sd_dist(settings[0],
                                      stations)  # figure out stations target(i.e. their surplus and deficit)
            users = dist_users(variance, stations)
            compare_curr(stations, users, None)
            reset_users(users)
            compare_curr(stations, users, settings[1])
            break
        else:
            print('select again')
    plt.show()
    """stations = load_stations()  # loads stations, their target = curr
    # filter_stations(stations, 1000, t)  # filters out farther stations
    variance = create_sd_dist(settings[0], stations)    # figure out stations target(i.e. their surplus and deficit)
    users = dist_users(variance, stations)

    compare_curr(stations, users)"""


def compare_curr(stations, users, constraint):
    stats_sum = []
    stats_avg = []
    stats_dist = []
    index = np.arange(len(users) + 1)

    for x in range(6):  # runs algorithm with different prio, starts fresh each time
        stats = run_curr(stations, users, x, constraint)  # run alg and gather data for priority x
        stats_sum.append(stats[0])  # fill data into arrays to use to create plots
        stats_avg.append(stats[1])
        stats_dist.append(stats[2])
        reset_users(users)  # reset users back to original positions

    stats_sum = np.array(stats_sum)
    stats_avg = np.array(stats_avg)
    stats_dist = np.array(stats_dist)

    print(stats_sum)
    create_dist_plot(index, stats_dist)  # create plot here


def run_curr(stations, users, p, constraint):
    sum = StationsDiff(stations)  # get sum of stations difference in stock before run
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    avg = sum / len(stations)  # avg difference, per run

    stats_sum = [sum]
    stats_avg = [avg]
    stats_dist = [dist_rr]

    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            distribute(stations, p, constraint)  # runs algorithm, rerouting a single user then recording data
        else:
            print('stations MEET targets')

        sum = StationsDiff(stations)  # get sum of stations difference in stock
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_sum, stats_avg, stats_dist]


def test():
    s = Station()
    s1 = Station()
    s2 = Station()

    stations = [s, s1, s2]
    users = create_rand_users(stations,5)

    s.print_info()
    s1.print_info()
    s2.print_info()
    print(s.getdiff()+s1.getdiff()+s2.getdiff())
    delete_inc(stations)
    users = create_rand_users(stations, 5)

    s.print_info()
    s1.print_info()
    s2.print_info()
    print(s.getdiff() + s1.getdiff() + s2.getdiff())

""""
# s = create_rand_stations(0.000000, 0.000000, 1000, 10)
t = (39.953555, -75.164042)
s = load_stations()
# print(len(s))
filter_stations(s, 1000, t)
# print(len(s))

for x in s:
    print(x.getdiff())
variance = create_sd_dist(10, s)
print(variance)
dist_users(variance, s)
for x in s:
    print(x.getdiff())
"""

startup()


