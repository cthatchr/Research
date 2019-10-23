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
from Random import *
from Real import *
from Completion import *


def startup():
    choice = {}
    choice['1'] = "Random Data"
    choice['2'] = "Real Data"
    choice['3'] = "Completion"
    choice1 = {}
    choice1['1'] = "Greedy"
    choice1['2'] = "Min Cost Flow"
    choice1['3'] = "Compare Both"

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

            while True:
                options = choice1.keys()
                for x in options:
                    print(x, choice1[x])

                selection = input("Select:")
                if selection == '1':  # greedy
                    greedy_settings()
                    break
                elif selection == '2':  # mcf
                    mcf_settings()
                    break
                elif selection == '3':  # both
                    mcf_greedy_settings()
                    break
                else:
                    print('select again')
            break
        else:
            print('select again')


def test():
    stations = load_stations()
    users = 150  # the amount of users we plan the create and reroute
    amt = len(stations)
    s = np.random.uniform(-1, 1, size=amt)
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
station_map_scale()

