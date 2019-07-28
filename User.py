import random
from Station import *
from geopy import distance
import pandas as pd
from datetime import datetime, date, time, timedelta

class User:
    def __init__(self, id='U', start=0, end=0, rerouted=False):
        self.id = id  # id, u1..
        self.start = start  # start station
        self.end = end  # destination station
        self.rr_end = None  # new destination(rerouted station)
        self.rerouted = rerouted  # marks if a user was already rerouted

    def createRandUser(self, stations):
        # assign random id if not given
        if self.id == 'U':
            self.id = 'U%03x' % random.randrange(16 ** 3)

        randstart = random.randint(0, len(stations)-1)
        randdest = random.randint(0, len(stations)-1)
        # if start and dest are the same re roll until not the same
        while randstart == randdest:
            randstart = random.randint(0, len(stations)-1)
            randdest = random.randint(0, len(stations)-1)

        self.start = stations[randstart]
        self.end = stations[randdest]
        self.rerouted = False

        # add user to incoming for station
        # print(self)
        self.end.inc.append(self)

    def printuser(self):
        return 'ID: ' + self.id, 'Start: ' + self.start.id, 'Destination: ' + self.end.id

    def getDist(self):
        if self.rr_end is None:
            return 0
        else:
            x = (self.end.lat, self.end.lon)
            y = (self.rr_end.lat, self.rr_end.lon)
            return distance.distance(x, y).meters


def create_rand_users(stations, amount):
    users = []
    # print("Creating", amount, 'users.')
    for x in range(amount):
        id = 'U' + str(x + 1)
        # create user
        u = User(id=id)
        u.createRandUser(stations)
        users.append(u)
    return users

def load_users(stations, time_interval):
    users = []
    count = 0
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('indego-trips-2019-q1.csv')  # load users

    strt = rand_date(df)  # creates a random date to start from
    end = strt + timedelta(minutes=time_interval)  # random end based on strt and time interval given(in minutes)

    # filters rows between these two start and end times
    df = df[df['start_time'].between(
        strt.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'))]

    for index, row in df.iterrows():  # loops through each record of user
        s = get_station_by_id(stations, row['start_station'])
        d = get_station_by_id(stations, row['end_station'])
        if d is None:
            count += 1
            continue
        u = User(id=row['trip_id'], start=s, end=d)
        users.append(u)
        u.end.inc.append(u)
    if count > 0:  # if users were not loaded due to out of date stations
        print(count, 'user(s) not loaded')
    return users


def total_RR_distance(users):  # gets the total distance users were rerouted from their original destinations
    total = 0
    for x in users:
        total += x.getDist()
    return total


def rand_date(df): # creates a random date between the start and end date
    start = datetime.strptime(df.iloc[0]['start_time'], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(df.iloc[len(df.index)-1]['start_time'], '%Y-%m-%d %H:%M:%S')
    diff = int((end - start).total_seconds()) # diff of seconds between first and last date
    sec = random.randint(0, diff) # creates random int in this diff and then adds to start time
    return start + timedelta(seconds=sec)


def print_users(users):
    for x in users:
        print(x.id)


def reset_users(users):  # resets the users so we can run the algorithm fresh
    for x in users:
        if x.rr_end is not None:  # resets as long as user was rerouted
            x.rr_end.inc.remove(x)  # remove user from rerouted stations incoming
            x.rr_end = None  # reset users rerouted station
            x.end.inc.append(x)  # add user back to original stations incoming
            x.rerouted = False
