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
from Completion import *


def startup():
    choice1 = {}
    choice1['1'] = "Greedy"
    choice1['2'] = "Min Cost Flow"
    choice1['3'] = "Compare Both"

    while True:
        options = choice1.keys()
        for x in options:
            print(x, choice1[x])

        selection = input("Select:")
        settings = choose_settings()  # set the settings

        if selection == '1':  # greedy
            stats = run(settings, 'G')
            if settings[3][0] is True:
                avg = greedy_average(stats[:][0])
                constraint_avg = greedy_average(stats[:][1])
                compare_dist(np.arange(settings[0]+1), avg, constraint_avg)
                print('Greedy Average')
                print('No Constraint:', greedy_lowest_dist(avg))
                print('Constraint:', greedy_lowest_dist(constraint_avg))
            else:
                average = greedy_average(stats)
                create_dist_plot(np.arange(settings[0]+1), average)
                print('Greedy Average')
                print('Best distance:', greedy_lowest_dist(average))
            break
        elif selection == '2':  # mcf
            stats = run(settings, 'M')
            if settings[3][0] is True:
                print('MCF Average')
                print('No Constraint:', mcf_average(stats[0]))
                print('Constraint:', mcf_average(stats[1]))
            else:
                print('MCF Average', mcf_average(stats[0]))
            break
        elif selection == '3':  # both
            stats = run(settings, 'B')
            if settings[3][0] is True:
                greedy_avg = greedy_average(stats[1][:][0])
                greedy_constraint_avg = greedy_average(stats[1][:][1])
                compare_dist(np.arange(settings[0]+1), greedy_avg, greedy_constraint_avg)
                print('MCF Average')
                print('No Constraint:', mcf_average(stats[0][0]))
                print('Constraint:', mcf_average(stats[0][1]))
                print('Greedy Average')
                print('No Constraint:', greedy_avg)
                print('Constraint:', )
            else:
                greedy_avg = greedy_average(stats[1])
                create_dist_plot(np.arange(settings[0] + 1), greedy_avg)
                print('MCF Average', mcf_average(stats[0]))
                print('Greedy Average')
                print('Best distance:', greedy_lowest_dist(greedy_avg))
            break
        else:
            print('select again')


def test1(s):
    stations = load_stations()
    users = 150  # the amount of users we plan the create and reroute
    amt = len(stations)

    '''s = np.random.exponential(size=amt)
    y = np.random.uniform(-1, 1, size=amt)
    for x in range(amt):
        if y[x] < 0:
            s[x] = -(s[x])'''
    # s = np.random.uniform(-1, 1, size=amt)
    totals = sd_totals(s)
    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
    ax1.hist(s, density=True)

    variance = np.zeros(amt)  # normalize distribution
    for x in range(len(s)):
        if s[x] > 0:  # if +
            variance[x] = (s[x] / totals[0])*150
        if s[x] < 0:  # if -
            variance[x] = -(s[x] / totals[1])*150
    ax2.hist(variance, density=True)

    totals = sd_totals(variance)
    print(totals)
    print(variance)

    def_amt = users
    sur_amt = users
    v = np.zeros(len(stations), dtype=int)

    for x in range(len(variance)):
        z = variance[x]
        if z > 0:
            r = np.fix(z)
            v[x] += r
            variance[x] -= r
            sur_amt -= r
        elif z < 0:
            r = np.fix(z)
            v[x] += r
            variance[x] -= r
            def_amt += r

    nt = sd_totals(variance)
    print(nt)
    print(sur_amt, def_amt)
    print(v)
    print(variance)
    ax3.hist(v, density=True)

    max = np.where(variance == np.amax(variance))
    min = np.where(variance == np.amin(variance))
    print(min, max)

    while (def_amt > 0) or (sur_amt > 0):  # while there is still variances to assign
        if sur_amt > 0:
            max = np.where(variance == np.amax(variance))
            v[max[0]] += 1
            variance[max[0]] = 0
            sur_amt -= 1
        if def_amt > 0:
            min = np.where(variance == np.amin(variance))
            v[min[0]] -= 1
            variance[min[0]] = 0
            def_amt -= 1

    nt = sd_totals(variance)
    print(nt)
    print(sur_amt, def_amt)
    print(v)
    print(variance)
    print(sd_totals(variance))
    ax4.hist(v, density=True)
    plt.show()

    '''# v = 2 * (np.random.random_sample(size=amt) - 0.5)

    v = sd_dist(users, stations, 'U')
    test_distribution(v)'''


def test2():
    stations = load_stations()
    users = 150  # the amount of users we plan the create and reroute
    amt = len(stations)
    sur_ex = 0
    def_ex = 0

    '''y = np.random.uniform(-1, 1, size=amt)
    pos = 0
    for i in y:
        if i > 0:
            pos += 1
    s1 = np.random.exponential(size=pos)
    s2 = -(np.random.exponential(size=(amt-pos)))
    s = np.append(s1,s2)
    random.shuffle(s)
    # print(s1,s2,s)'''

    s = 2 * ((np.random.random_sample(size=amt) - 0.5))
    totals = sd_totals(s)
    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
    ax1.hist(s, density=True)

    variance = np.zeros(amt)  # normalize distribution
    for x in range(len(s)):
        if s[x] > 0:  # if +
            variance[x] = (s[x] / totals[0])*150
        if s[x] < 0:  # if -
            variance[x] = -(s[x] / totals[1])*150
    ax2.hist(variance, density=True)

    totals = sd_totals(variance)
    print(totals)
    print(variance)

    def_amt = users
    sur_amt = users
    v = np.zeros(len(stations), dtype=int)

    for x in range(len(variance)):
        z = variance[x]
        if z > 0:
            r = round(z)
            v[x] += r
            sur_amt -= r
        elif z < 0:
            r = round(z)
            v[x] += r
            def_amt += r

    nt = sd_totals(variance)
    print(nt)
    print(sur_ex, def_ex)
    print(sur_amt, def_amt)
    print(v)
    print(variance)
    ax3.hist(v, density=True)

    while (def_amt > 0) or (sur_amt > 0):  # while there is still variances to assign
        r = np.random.randint(0, amt)
        if (sur_amt > 0) and (v[r] > 0):
            v[r] += 1
            sur_amt -= 1
        if (def_amt > 0) and (v[r] < 0):
            v[r] -= 1
            def_amt -= 1

    while (def_amt < 0) or (sur_amt < 0):  # while there is still variances to assign
        r = np.random.randint(0, amt)
        if (sur_amt < 0) and (v[r] > 0):
            v[r] -= 1
            sur_amt += 1
        if (def_amt < 0) and (v[r] < 0):
            v[r] += 1
            def_amt += 1

    nt = sd_totals(v)
    print(nt)
    print(sur_amt, def_amt)
    print(v)
    print(sd_totals(v))
    ax4.hist(v, density=True)
    plt.show()

    '''# v = 2 * (np.random.random_sample(size=amt) - 0.5)

    v = sd_dist(users, stations, 'U')
    test_distribution(v)'''

def sd_totals(s):
    sur_total = 0
    def_total = 0
    for x in s:
        if x > 0:
            sur_total += x
        if x < 0:
            def_total += x
    return [sur_total, def_total]


# s = load_df()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

startup()
