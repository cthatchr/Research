from geopy import distance
from Algorithm import *
from Station import *
from User import *
from DistList import *
import numpy as np
import matplotlib.pyplot as plt

def run(num_runs):
    mr_sum_A = 0
    mr_sum_B = 0
    mr_avg_A = 0
    mr_avg_B = 0
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

    while True:
        try:
            user_amount = int(input('How many users would you like to create?:'))
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            k = int(input('How many users are we allowed to move?:'))
            break
        except:
            print('Enter an integer.')

    # run j times
    for j in range(num_runs):
        stations = createStations(lat, lon, r, station_amount) # create stations
        users = createUsers(stations, user_amount) # create users

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
        # create averages from sums and amount fo stations
        avg_B = sum_B / len(stations)
        avg_A = sum_A / len(stations)
        # print results
        print_results(sum_B, sum_A, avg_B, avg_A, run=j+1)

        # multi run results
        mr_sum_B += sum_B
        mr_sum_A += sum_A
        mr_avg_B += avg_B
        mr_avg_A += avg_A

    # calculate multi run results and print them
    mr_sum_B = mr_sum_B / num_runs
    mr_sum_A = mr_sum_A / num_runs
    mr_avg_B = mr_avg_B / num_runs
    mr_avg_A = mr_avg_A / num_runs
    print_results(mr_sum_B, mr_sum_A, mr_avg_B, mr_avg_A, run=0)
    # would at this point turn this data into a plot point on the line graph
    # turn into a list, @D array or point

    #create bar graph
    before = {mr_sum_B, mr_avg_B}
    after = (mr_sum_A, mr_avg_A)
    create_barplot(before, after)


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

def create_lineplot(bef, aft):
    # create a line plot given a set of data
    print()

def test():
    s1 = Station(id='s1', target=1)
    s = [s1]
    distribute(s, 1)

while True:
    try:
        j = int(input('Number of tests run:'))
        break
    except:
        print('Enter an integer.')
run(j)


