import random
import math
import json
import pandas as pd
from geopy import distance
from pandas.io.json import json_normalize
import numpy as np
from DistList import *

class Station:
    def __init__(self, id='S', lat=0, lon=0, max=10, curr=0, target=2):
        self.id = id  # id, d1,d2
        self.lat = lat  # longitude
        self.lon = lon # latitude
        self.max = max  # max bikes it can hold
        self.curr = curr  # current amount of bikes
        self.target = target # target amount
        self.inc = [] # list of incoming bikes

    def rand_coord(self, targetLat, targetLon, radius):
        y0 = targetLat
        x0 = targetLon
        rd = radius / 111300
        u = random.random()
        v = random.random()
        w = rd * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        newlat = y + y0;
        newlon = x + x0;
        self.lat = newlat
        self.lon = newlon

        # randomize id if not given one
        if self.id == 'S':
            self.id = 'S%03x' % random.randrange(16 ** 3)

    def getdiff(self, absval=False):  # gets the difference of stock for the station, can get the absolute value as well
        if absval is False:
            return (self.curr + len(self.inc)) - self.target
        else:
            return abs((self.curr + len(self.inc)) - self.target)

    def print_info(self):
        print(self.id, self.lat,self.lon)
        print('Current:', self.curr)
        print('Incoming:', len(self.inc), end=' ')
        if len(self.inc) is 0:
            print('()')
        else:
            print('(', end='')
            for y in range(len(self.inc)):
                if y is len(self.inc) - 1:
                    print(self.inc[y].id, end=')\n')
                else:
                    print(self.inc[y].id, end=' ')
        print('Target:', self.target)
        print('Max:', self.max)
        print('Difference:', -self.getdiff())
        print('')

    # returns true if there is a reroutable user
    def has_rr_user(self):
        check = False
        for x in self.inc:
            if x.rerouted is False:
                check = True
        return check

    # returns the first reroutable user in the list
    def get_rr_user(self):
        for z in self.inc:
            if z.rerouted is False:
                return z

    def is_surplus_or_deficit(self):  # returns d if deficit, s if surplus, 0 if no diff
        if self.getdiff() > 0:  # if surplus
            return 's'
        elif self.getdiff() < 0:  # if deficit
            return 'd'
        elif self.getdiff() == 0:  # no diff
            return 0

    def is_surplus(self):
        if self.getdiff() > 0:
            return True
        else:
            return False

    def is_deficit(self):
        if self.getdiff() < 0:
            return True
        else:
            return False


def load_df():
    with open('indego_stationdata.json') as d:  # reads json data from file
        data = json.load(d)
    df = pd.DataFrame(data['features'])  # turns json data into Dataframe to work off of
    dfd = json_normalize(df['properties'])  # normalizes json data
    for index, row in dfd.iterrows():  # loops through each record of station
        # print(row['kioskId'])
        if row['kioskId'] in [3183, 3186, 3181, 3188, 3117, 3111]:  # filtering
            dfd.drop(index, inplace=True)
    return dfd

def load_plot_stations():
    with open('indego_stationdata.json') as d:  # reads json data from file
        data = json.load(d)
    df = pd.DataFrame(data['features'])  # turns json data into Dataframe to work off of
    dfd = json_normalize(df['properties'])  # normalizes json data

    stations = load_stations()
    filter_stations(stations, 2000, (39.953555, -75.164042))

    for index, row in dfd.iterrows():  # loops through each record of station
        # print(row['kioskId'])
        if row['kioskId'] not in [s.id for s in stations]:  # filtering
            dfd.drop(index, inplace=True)
    return dfd


def load_stations():  # loads stations from json data
    stations = []
    with open('indego_stationdata.json') as d:  # reads json data from file
        data = json.load(d)
    dfd = json_normalize(data, record_path='features')  # normalizes json data
    df = pd.DataFrame(dfd)  # turns json data into Dataframe to work off of
    for index, row in df.iterrows():  # loops through each record of station
        s = Station(id=row['properties.kioskId'],
                    lat=row['properties.latitude'],
                    lon=row['properties.longitude'],
                    max=row['properties.totalDocks'],
                    curr=row['properties.bikesAvailable'],
                    target=row['properties.bikesAvailable'])
        if s.id not in [3183, 3186, 3181, 3188, 3117, 3111]: # filtering
            stations.append(s)

    return stations


def filter_stations(stations, filter, target):
    stations[:] = [y for y in stations if distance.distance((y.lat, y.lon), target).meters < filter]


def stations_has_rr_user(stations):  # checks if ANY of the stations have a reroutable user, true if they do
    check = False
    for x in stations:
        if x.has_rr_user():
            check = True
    return check


def get_station_by_id(stations, id):
    for x in stations:
        if x.id == id:
            return x
            break


def sd_dist(amount, stations, type = 'U'):
    amt = len(stations)
    users = amount  # the amount of users we plan the create and reroute
    sur_total, def_total, sur_ex, def_ex = 0, 0, 0, 0
    def_amt, sur_amt = users, users

    if type is 'U':  # uniform
        s = np.random.uniform(-1, 1, size=amt)
    elif type is 'N':  # normal
        s = np.random.normal(0, (users / amt) * 1.5, size=amt)
    elif type is 'R':
        s = 2 * ((np.random.random_sample(size=amt) - 0.5))
    elif type is 'E':
        y = np.random.uniform(-1, 1, size=amt)
        pos = 0
        for i in y:
            if i > 0:
                pos += 1
        s1 = np.random.exponential(size=pos)
        s2 = -(np.random.exponential(size=(amt - pos)))
        s = np.append(s1, s2)
        random.shuffle(s)

    totals = sd_totals(s)
    sur_total = totals[0]
    def_total = totals[1]

    v = np.zeros(amt)  # normalize distribution
    for x in range(len(s)):
        if s[x] > 0:  # if +
            v[x] = (s[x] / sur_total)*users
        elif s[x] < 0:  # if -
            v[x] = -(s[x] / def_total)*users

    for x in range(len(v)):  # round each float to an int
        z = v[x]
        if z > 0:
            v[x] = round(v[x])
            sur_amt -= v[x]
        elif z < 0:
            v[x] = round(v[x])
            def_amt += v[x]

    while (def_amt > 0) or (sur_amt > 0):  # while there is still variances to assign
        r = np.random.randint(0, amt)
        if (sur_amt > 0) and (v[r] >= 0):
            v[r] += 1
            sur_amt -= 1
        if (def_amt > 0) and (v[r] <= 0):
            v[r] -= 1
            def_amt -= 1

    while (def_amt < 0) or (sur_amt < 0):  # while were to many variances assigned
        r = np.random.randint(0, amt)
        if (sur_amt < 0) and (v[r] > 0):
            v[r] -= 1
            sur_amt += 1
        if (def_amt < 0) and (v[r] < 0):
            v[r] += 1
            def_amt += 1
    return v.astype(int)


def sd_totals(s):
    sur_total = 0
    def_total = 0
    for x in s:
        if x > 0:
            sur_total += x
        if x < 0:
            def_total += x
    return [sur_total, def_total]


def create_sd_dist_old(amount, stations):  # returns an array which represents each stations surplus and deficit
    v = np.zeros(len(stations), dtype=int)
    def_amt = amount
    sur_amt = amount
    while (def_amt > 0) or (sur_amt > 0):  # while there is still variances to assign
        num = np.random.randint(len(stations))  # randomly choose a 'station' to iterate + or -
        if v[num] == 0:  # if no variance is set,
            if (def_amt > 0) and (sur_amt > 0):  # randomly choose + or -
                ht = np.random.randint(2)
            elif def_amt is 0:  # if no more deficit iters, choose surplus
                ht = 1
            elif sur_amt is 0:  # if no more surplus iters, choose deficit
                ht = 0

            if ht is 1:  # choose as surplus while there is remaining amt
                v[num] += 1
                sur_amt -= 1
            elif ht is 0:  # choose as deficit while there is remaining amt
                v[num] -= 1
                def_amt -= 1

        elif (v[num] > 0) and (sur_amt > 0) :  # if variance is already surplus
            v[num] += 1
            sur_amt -= 1
        elif (v[num] < 0) and (def_amt > 0):  # if variance is already deficit
            v[num] -= 1
            def_amt -= 1
    return v


def delete_inc(stations):  # deletes incoming users from stations
    for x in stations:
        x.inc.clear()


def get_average_distance(stations):
    distance_sum = 0
    for x in range(len(stations)):
        for y in range(1,len(stations)):
                distance_sum += distance.distance((stations[x].lat, stations[x].lon), (stations[y].lat, stations[y].lon)).meters
    average = distance_sum/(len(stations)*(len(stations)-1))
    return average

'''
def get_average_distance(stations):
    distance_sum = 0
    for x in stations:
        dl = DistList(0)
        dl.fill_distance(stations, x)
        for y in dl.distList:
            distance_sum += y.dist
    average = distance_sum/(len(stations)*(len(stations)-1))
    return average
'''

def get_distance(st1, st2):
    loc1 = (st1.lat, st1.lon)
    loc2 = (st2.lat, st2.lon)
    return distance.distance(loc1, loc2).meters