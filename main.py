from geopy import distance
from Algorithm import *
from Station import *
from User import *
from DistList import *
import numpy as np
import matplotlib.pyplot as plt

def startup():
    settings = []

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

    print(settings[2], settings[3])
    run(settings)


def run(settings):
    stats_sum = []
    stats_avg = []
    index = []
    k_sum_B = 0
    k_avg_B = 0
    k_sum_A = 0
    k_avg_A = 0

    targ = Station(lat=40.7127, lon=-74.0059) # target is NYC

    for k in range(settings[2]+1): # setting that changes, meaning x axis value, users moved with each setting

        for j in range(settings[3]): # run test with same settings, j times, get stats for each
            stations = createStations(targ.lat, targ.lon, 2000, settings[0]) # create stations
            users = createUsers(stations, settings[1]) # create users

            j_sum_B = StationsDiff(stations) # get sum of stations difference in stock before, per test
            distribute(stations, k)  # runs algorithm, rerouting a maximum of k users
            j_sum_A = StationsDiff(stations) # get sum of stations difference in stock after, per test

            j_avg_B = j_sum_B/len(stations)  # avg difference, per test
            j_avg_A = j_sum_A/len(stations) # avg difference, per test

            k_sum_B += j_sum_B  # add to k's increment sum
            k_sum_A += j_sum_A  # add to k's increment sum
            k_avg_B += j_avg_B  # add to k's increment avg
            k_avg_A += j_avg_A # add to k's increment avg

        k_sum_B = k_sum_B/settings[3]
        k_avg_B = k_avg_B/settings[3]
        k_sum_A = k_sum_A/settings[3]
        k_avg_A = k_avg_A/settings[3]

        index.append(k)
        stats_sum.append([k_sum_B, k_sum_A])
        stats_avg.append([k_avg_B, k_avg_A])

    for x in index:
        print(x, stats_sum[x][0], stats_sum[x][1])
    create_lineplot(index, stats_sum, stats_avg) # create plot here


def create_barplot(bef, aft):
    fig, ax = plt.subplots()
    width = 0.35
    index = np.arange(len(bef))
    before = ax.bar(index - width/2, bef, width, color='r', label='Before', data=bef)
    after = ax.bar(index + width/2, aft, width, color='g', label='After', data=aft)

    ax.set_xlabel('Before/After Algorithm')
    ax.set_ylabel('Stock Difference')
    ax.set_title('Stock Difference Between Target and Current')
    ax.set_xticks(index)
    ax.set_xticklabels(('Sum', 'Average'))
    ax.legend()
    fig.tight_layout()
    plt.show()

def create_lineplot(index, sum, avg):
    # create a line plot given a set of data
    # plt.plot(stats, label='sum')
    plt.plot(index, sum[0:])
    plt.plot(index, avg[0:])
    plt.show()

def test():
    s1 = Station(id='s1', target=1)
    s = [s1]
    distribute(s, 1)

startup()


