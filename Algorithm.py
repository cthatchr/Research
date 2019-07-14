from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *

def distribute(stations, k):
    i = 0
    rr_counter = 0
    target = None
    # distribute k users
    while i < k:
        # check if every station meets target if so then theres no need to redistribute
        if meetsTarget(stations):
            # if stations meet target then stop distribution
            # print("All stations meet target. STOPPED")
            break
        # loop through stations to SET TARGET STATION
        for x in stations:
            # set target station to one farthest from target amount
            if target is None:
                # print('Target is now station:', x.id)
                target = x
            elif x.getdiff() > target.getdiff():
                # print('Target is now station:', x.id)
                target = x
        # create list of stations with distance pairings near target
        # print("\nTarget station: ", target.id)
        dl = DistList()
        dl.distFill(stations, target)
        dlist = dl.distList
        # dl.printList()
        # print('')

        # if there are no stations with reroutable users then the algorithm stops
        if stations_has_rr_user(stations) is False:
            # print('There are no more reroutable users. STOPPED.')
            break

        # loop through distlist to FIND STATION TO REROUTE FROM
        # ASSIGN STATION TO REROUTE FROM if priority is larger than others and station has incoming users that can be rerouted
        rr = None
        for y in dlist:
            # checks if the station has an incoming reroutable user, skips otherwise
            if y.station.has_rr_user() is False:
                continue

            # if not already assigned then assign
            if rr is None:
                rr = y
            # otherwise only choose the lowest priority station
            elif (y.priority < rr.priority):
               rr = y

        # if there are no stations to take reroutable users from, i.e. target station has the only ones, stop algorithm
        if rr is None:
            # print('There are no more reroutable users. STOPPED')
            break

        # assign rerouted station from distance pairings
        rr_station = rr.station

        # get incoming user to reroute to target station
        rr_user = rr_station.get_rr_user()

        # print('Rerouting user', rr_user.id, 'from station', rr_station.id, 'to', target.id)
        # reroute user to target station(remove+append), mark them rerouted and increment k
        rr_station.inc.remove(rr_user)
        target.inc.append(rr_user)
        rr_user.rerouted = True
        rr_counter += 1  # counts how many users have been reoruted

        # prints all information including incoming users for all stations
        """print('')
        for x in range(len(stations)):
            stations[x].display_info()
        print('')"""
        i += 1

    # print('Algorithm has redistributed', rr_counter, 'users. DONE')

def distribute_incr(stations, k=1):
    i = 0
    rr_counter = 0
    target = None
    # distribute k users
    while i < k:
        # check if every station meets target if so then theres no need to redistribute
        if meetsTarget(stations):
            # if stations meet target then stop distribution
            # print("All stations meet target. STOPPED")
            break
        # loop through stations to SET TARGET STATION
        for x in stations:
            # set target station to one farthest from target amount
            if target is None:
               # print('Target is now station:', x.id)
                target = x
            elif x.getdiff() > target.getdiff():
               # print('Target is now station:', x.id)
                target = x
        # create list of stations with distance pairings near target
        # print("\nTarget station: ", target.id)
        dl = DistList()
        dl.distFill(stations, target)
        dlist = dl.distList
        # dl.printList()
        # print('')

        # if there are no stations with reroutable users then the algorithm stops
        if stations_has_rr_user(stations) is False:
            # print('There are no more reroutable users. STOPPED.')
            break

        # loop through distlist to FIND STATION TO REROUTE FROM
        # ASSIGN STATION TO REROUTE FROM if priority is larger than others and station has incoming users that can be rerouted
        rr = None
        for y in dlist:
            # checks if the station has an incoming reroutable user, skips otherwise
            if y.station.has_rr_user() is False:
                continue

            # if not already assigned then assign
            if rr is None:
                rr = y
            # otherwise only choose the lowest priority station
            elif (y.priority < rr.priority):
                rr = y

        # if there are no stations to take reroutable users from, i.e. target station has the only ones, stop algorithm
        if rr is None:
            # print('There are no more reroutable users. STOPPED')
            break

        # assign rerouted station from distance pairings
        rr_station = rr.station

        # get incoming user to reroute to target station
        rr_user = rr_station.get_rr_user()

        # print('Rerouting user', rr_user.id, 'from station', rr_station.id, 'to', target.id)
        # reroute user to target station(remove+append), mark them rerouted and increment k
        rr_station.inc.remove(rr_user)
        target.inc.append(rr_user)
        rr_user.rerouted = True
        rr_counter += 1  # counts how many users have been reoruted

        # prints all information including incoming users for all stations
        # print('')
        """for x in range(len(stations)):
            stations[x].display_info()
        print('')"""
        i += 1

    # print('Algorithm has redistributed', rr_counter, 'users. DONE')

# gets the sum/avg diff of an algorithm run before/after
def print_results(sum_B, sum_A, avg_B, avg_A, run):
    if run is 0:
        print("Multi-run Results")
    else:
        print('Run #', run)
    print('Before:')
    print('Sum:', sum_B)
    print("Average:", avg_B)
    print('After:')
    print('Sum:', sum_A)
    print("Average:", avg_A)

def meetsTarget(stations):
    check = False
    for x in stations:
        if x.curr + len(x.inc) >= x.target:  # if station is above targetabove target
            check = True
        else:
            check = False
            break
    return check

# get sum of all stations difference between current and target stock
def StationsDiff(stations):
    total = 0
    for x in range(len(stations)):
        total += stations[x].getdiff(absval=True)
    return total

# get sum of total distance users were relocated between stations
# def UsersDiff(stations):