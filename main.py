from geopy import distance
from Algorithm import *
from Station import *
from User import *
from DistList import *
import numpy as np
import matplotlib.pyplot as plt

def run():
    # target is NYC
    lat = 40.7127
    lon = -74.0059
    r = 2000
    targ = Station(lat=lat, lon=lon)

    while True:
        try:
            station_amount = int(input('How many stations would you like to create?:'))
            break
        except:
            print('Enter an integer.')
    # create stations
    stations = createStations(lat,lon,r,station_amount)

    while True:
        try:
            user_amount = int(input('How many users would you like to create?:'))
            break
        except:
            print('Enter an integer.')
    # create users
    users = createUsers(stations, user_amount)

    # prints all information including incoming users for all stations
    for x in range(len(stations)):
        stations[x].display_info()


def createGraph(bef, aft):
    n = 2
    bar_width = 0.35
    index = np.arange(n)
    before = plt.bar(index, bef, bar_width, color='r',label='Before')
    after = plt.bar(index + bar_width, aft, bar_width, color='g',label='After')

    plt.xlabel('Before/After Algorithm')
    plt.ylabel('Stock Difference')
    plt.title('Stock Difference Between Target and Current')
    plt.xticks(index + bar_width, ('Sum', 'Average'))
    plt.legend()
    plt.tight_layout()
    plt.show()

run()












# test()
def test():
    lat = 40.7127
    lon = -74.0059
    r = 2000
    targ = Station(lat=lat,lon=lon)

    # create stations
    s1 = Station(id='s1', target=1)
    s2 = Station(id='s2', target=5)
    s3 = Station(id='s3', target=3)
    # s4 = Station(id='s4')
    # s5 = Station(id='s5')
    stations = [s1, s2, s3]
    # randomize stations
    for x in range(len(stations)):
        s = stations[x]
        s.randstation(lat, lon, r)

    # create distance list and print it
    # dl = DistList()
    # dl.distFill(stations, targ)
    # print(targ.lat,targ.lon)
    # dl.printList()

    # create users
    u1 = User(id='u1')
    u2 = User(id='u2')
    u3 = User(id='u3')
    u4 = User(id='u4')
    u5 = User(id='u5')
    u6 = User(id='u6')
    # u7 = User(id='u7')
    # u8 = User(id='u8')
    users = [u1, u2, u3, u4, u5, u6]
    # randomize Users
    for x in range(len(users)):
        u = users[x]
        u.createRandUser(stations)
        print(u.printuser())

    # prints incoming users for all stations
    for x in range(len(stations)):
        print(stations[x].id + ' incoming users: ')
        for y in range(len(stations[x].inc)):
            print(stations[x].inc[y].id)

# runs algorithm, rerouting a maximum of k users
    k = 3

    # get sum of stations difference in stock before and after Algorithm is run
    sdiffB = StationsDiff(stations)
    distribute(stations, k)
    sdiffA = StationsDiff(stations)

    print('Diff B:', sdiffB)
    print('Diff A:', sdiffA)

    avgB = sdiffB/len(stations)
    avgA = sdiffA/len(stations)

    before = {sdiffB, avgB}
    after = (sdiffA, avgA)
    createGraph(before, after)