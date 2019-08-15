import random
import math
import json
import pandas as pd
from pandas.io.json import json_normalize

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


# creates n amount of stations around a target coordinate
def create_rand_stations(lat, lon, radius, amount, distribution_type=4, max=10):
    stations = []
    for x in range(amount):
        id = 'S' + str(x+1)
        # gives a random current amount between 0 and max (can be changed)
        curr = random.randint(0, max-1)
        # gives a random target amount between 3 and max-2 (can be changed)
        targ = random.randint(3, max)
        # create Station
        s = Station(id=id, target=targ, curr=curr)
        s.rand_coord(lat, lon, radius)
        stations.append(s)
    return stations


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
                    curr=row['properties.bikesAvailable'])
        stations.append(s)
    return stations


def set_stations_t_distr(stations, target_distr_type=4):
    for x in stations:
        set_target_distribution(x, target_distr_type)


def set_stations_c_distr(stations, curr_distr_type=4):
    for x in stations:
        set_curr_distribution(x, curr_distr_type)

# checks if ANY of the stations have a reroutable user, true if they do
def stations_has_rr_user(stations):
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


def set_target_distribution(station, dist_type):  # sets stations target amount; low, medium, high, or random
    max = station.max
    half = int(round(max/2))
    if dist_type is 1:  # low 0-half
        station.target = random.randint(0, half)

    elif dist_type is 2:  # med 1/4-3/4
        lower = int(round(half/2))
        upper = int(round(half + lower))
        station.target = random.randint(lower, upper)

    elif dist_type is 3:  # high half-max
        station.target = random.randint(half, max)

    elif dist_type is 4:  # random 0-max
        station.target = random.randint(0, max)


# might want to add current distribution that works off of the target amount***
def set_curr_distribution(station, dist_type):  # sets stations current amount; low, medium, high, or random
    max = station.max
    half = int(round(max/2))
    if dist_type is 1:  # low 0-half
        station.curr = random.randint(0, half)

    elif dist_type is 2:  # med 1/4-3/4
        lower = int(round(half/2))
        upper = int(round(half + lower))
        station.curr = random.randint(lower, upper)

    elif dist_type is 3:  # high half-max
        station.curr = random.randint(half, max)

    elif dist_type is 4:  # random 0-max
        station.curr = random.randint(0, max)


def delete_inc(stations):
    for x in stations:
        x.inc.clear()