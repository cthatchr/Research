import random
import math

class Station:
    def __init__(self, id='S', lat=0, lon=0, max=10, curr=0, target=2):
        self.id = id  # id, d1,d2
        self.lat = lat  # longitude
        self.lon = lon # latitude
        self.max = max  # max bikes it can hold
        self.curr = curr  # current amount of bikes
        self.target = target # target amount
        self.inc = [] # list of incoming bikes

    def randstation(self, targetLat, targetLon, radius):
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

    def print_coord(self):
        return self.id, self.lat, self.lon

    # gets the difference of stock for the station, can get the absolute value as well
    def getdiff(self, absval=False):
        if absval == False:
            return self.target - self.curr - len(self.inc)
        else:
            return abs(self.target - self.curr - len(self.inc))

    def display_info(self):
        print(self.id)
        print('Current:', self.curr)
        print('Target:', self.target)
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

        print('Difference:', self.getdiff())
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
def createStations(lat, lon, radius, amount, max=10):
    stations = []
    # print('Creating', amount, 'stations.')
    for x in range(amount):
        id = 'S' + str(x+1)
        # gives a random current amount between 0 and max (can be changed)
        curr = random.randint(0, max-1)
        # gives a random target amount between 3 and max-2 (can be changed)
        targ = random.randint(3, max)
        # create Station
        s = Station(id=id, target=targ, curr=curr)
        s.randstation(lat, lon, radius)
        stations.append(s)
    return stations

# checks if ANY of the stations have a reroutable user, true if they do
def stations_has_rr_user(stations):
    check = False
    for x in stations:
        if x.has_rr_user():
            check = True
    return check



