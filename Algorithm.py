from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *


def distribute_random(stations, priority=0, k=1):
    i = 0
    target = None
    # distribute k users
    while i < k:
        # check if every station meets target if so then theres no need to redistribute
        if meetsTarget(stations):
            break
        # loop through stations to SET TARGET STATION
        for x in stations:
            # set target station to one farthest from target amount
            if target is None:
                target = x
            elif x.getdiff() < target.getdiff():
                target = x
        # create list of stations with distance pairings near target
        dl = DistList()
        dl.fill(stations, target)
        if priority == 2:  # changes priority if assigned
            dl.changePriority()
        dlist = dl.distList

        # if there are no stations with reroutable users then the algorithm stops
        if stations_has_rr_user(stations) is False:
            break
        # loop through distlist to FIND STATION TO REROUTE FROM
        # ASSIGN STATION TO REROUTE FROM if priority is larger than others and station has incoming users that can be rerouted
        rr = None
        for y in dlist:
            # checks if the station has an incoming reroutable user, skips otherwise
            if y.station.has_rr_user() is True:
                # if not already assigned then assign
                if rr is None:
                    rr = y
                # otherwise only choose the lowest priority station
                elif y.priority > rr.priority:
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
        rr_user.rr_end = target
        rr_user.rerouted = True



def distribute_real(stations, priority=0, ):
    target = None
    # loop through stations to SET TARGET STATION
    for x in stations:  # set target station to one farthest from target amount, lowest diff
        if target is None:
            target = x
            # print('target is now', target.id,'with a difference of',target.getdiff())
        elif x.getdiff() < target.getdiff():
            target = x
            # print('target is now', target.id, 'with a difference of', target.getdiff())
    # print('Final target is', target.id)
    # create list of stations with distance pairings near target
    dl = DistList()
    dl.fill(stations, target)
    if priority == 2:  # changes priority if assigned
        dl.changePriority()
    dlist = dl.distList

    if stations_has_rr_user(stations) is False: # if no stations with reroutable users then the algorithm stops
        return

    # ASSIGN STATION TO REROUTE FROM if priority is smaller than others and station has incoming users that can be rerouted
    rr = None
    for y in dlist:  # checks if the station has an incoming reroutable user, skips otherwise
        if y.station.has_rr_user() is True:
            if rr is None:  # if not already assigned then assign
                rr = y
                # print('rr is now', rr.station.id, 'with a priority of', rr.priority, 'and diff of', rr.station.getdiff())
            elif y.priority > rr.priority:  # otherwise only choose the lowest priority station
                rr = y
                # print('rr is now', rr.station.id, 'with a priority of', rr.priority, 'and diff of', rr.station.getdiff())

    # if there are no stations to take reroutable users from, i.e. target station has the only ones, stop algorithm
    if rr is None:
        print('not rerouting')
        return
    # print('final rr is ', rr.station.id, 'with a priority of', rr.priority)
    rr_station = rr.station  # assign rerouted station from distance pairings
    rr_user = rr_station.get_rr_user()  # get incoming user to reroute to target station

    # reroute user to target station(remove+append), mark them rerouted and increment k
    print('rerouting')
    rr_station.inc.remove(rr_user)
    target.inc.append(rr_user)
    rr_user.rr_end = target
    rr_user.rerouted = True


def meetsTarget(stations):
    check = False
    for x in stations:
        if (x.curr + len(x.inc)) >= x.target:  # if station meets target amount
            check = True
        elif (x.curr + len(x.inc)) < x.target:
            check = False
            break
    return check


# get sum of all stations difference between current and target stock
def StationsDiff(stations):
    total = 0
    for x in stations:
        total += x.getdiff(absval=True)
    return total