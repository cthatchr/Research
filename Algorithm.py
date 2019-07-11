from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *

def distribute(stations, k):
    i=0
    target = None
    # distribute k users
    while (i < k):
        # check if every station meets target if so then theres no need to redistribute
        if meetsTarget(stations):
            # if stations meet target then stop distribution
            print("All stations meet target. DONE")
            break
        # loop through stations to SET TARGET STATION
        for x in stations:
            # set target station to one farthest from target amount
            if target is None:
                print('Target is now station:', x.id)
                target = x
            elif x.getdiff() > target.getdiff():
                print('Target is now station:', x.id)
                target = x
        # create list of stations with distance pairings near target
        print("Target station: ", target.id)
        dl = DistList()
        dl.distFill(stations, target)
        dlist = dl.distList
        dl.printList()
        # loop through distlist to FIND STATION TO REROUTE FROM
        rr = None
        for y in dlist:
            # ASSIGN STATION TO REROUTE FROM if priority is larger than others and station has incoming users that can be rerouted
            s = y.station.inc
            if rr is None:
                # check if station has rerouteable users
                for z in s:
                    # if there is a user that has not been rerouted then assign as rerouteable
                    if z.rerouted is False:
                        rr = y
                        break
            elif (y.priority < rr.priority):
                # check if station has rerouteable users
                for z in s:
                    # if there is a user that has not been rerouted then assign as rerouteable
                    if z.rerouted is False:
                        rr = y
                        break
        # assign rerouted station from distance pairings
        rrst = rr.station
        inc = rrst.inc
        # print('Rerouting from station:', rrst.id, 'to target station:', target.id)
        # find incoming user to reroute to target station
        for t in inc:
            if t.rerouted is False:
                rruser = t
                break
        # reroute user to target station(remove+append), mark them rerouted and increment k
        print('Rerouting user', rruser.id, 'from station', rrst.id, 'to', target.id)
        inc.remove(rruser)
        target.inc.append(rruser)
        rruser.rerouted = True

        # prints incoming users for all stations
        for x in range(len(stations)):
            print(stations[x].id + ' incoming users: ')
            for y in range(len(stations[x].inc)):
                print(stations[x].inc[y].id)
        i += 1

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