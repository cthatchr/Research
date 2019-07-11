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

    while True:
        try:
            k = int(input('How many users are we allowed to move?:'))
            break
        except:
            print('Enter an integer.')

    # prints all information including incoming users for all stations
    for x in range(len(stations)):
        stations[x].display_info()
    print('')

    # get sum of stations difference in stock before Algorithm is run (get stats before)
    sum_B = StationsDiff(stations)

    # runs algorithm, rerouting a maximum of k users
    distribute(stations, k)

    # get sum of stations difference in stock after Algorithm (get stats after)
    sum_A = StationsDiff(stations)

    avg_B = sum_B / len(stations)
    avg_A = sum_A / len(stations)

    print('Before:')
    print('Sum:', sum_B)
    print("Average:", avg_B)
    print('After:')
    print('Sum:', sum_A)
    print("Average:", avg_A)

    before = {sum_B, avg_B}
    after = (sum_A, avg_A)
    createGraph(before, after)


def createGraph(bef, aft):
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

run()

def test():
    s1 = Station(id='s1', target=1)
    s = [s1]
    distribute(s, 1)


