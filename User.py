import random
from Station import *
from geopy import distance
import pandas as pd
from datetime import datetime, date, time, timedelta

class User:
    def __init__(self, id='U', start=0, dest=0, rerouted = False):
        self.id = id #id, u1..
        self.start = start #start station
        self.dest = dest #destination station
        self.rrdest = None  # new destination(rerouted station)
        self.rerouted = rerouted # marks if a user was already rerouted

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
        self.dest = stations[randdest]
        self.rerouted = False

        # add user to incoming for station
        # print(self)
        self.dest.inc.append(self)

    def printuser(self):
        return 'ID: ' + self.id, 'Start: ' + self.start.id, 'Destination: ' + self.dest.id

    def getDist(self):
        if self.rrdest is None:
            return 0
        else:
            x = (self.dest.lat, self.dest.lon)
            y = (self.rrdest.lat, self.rrdest.lon)
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
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('indego-trips-2019-q1.csv')  # load users

    strt = rand_date(df)  # creates a random date to start from
    end = strt + timedelta(minutes=time_interval)  # random end based on strt and time interval given(in minutes)

    # filters rows between these two start and end times
    df = df[df['start_time'].between(
        strt.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'))]

    for index, row in df.iterrows():  # loops through each record of user
        u = User(id=row['trip_id'],
                 start=get_station_by_id(stations, row['start_station']),
                 dest=get_station_by_id(stations, row['end_station']))
        users.append(u)
        u.dest.inc.append(u)
        # u.dest.print_info()
    return users

def total_RR_distance(users):
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
