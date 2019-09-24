from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *


def distribute_multiple_old(stations, priority=0, k=1):
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


def distribute_single(stations, priority):
    target = None
    # loop through stations to SET TARGET STATION
    for x in stations:  # set target station to one farthest from target amount, lowest diff
        if target is None:
            target = x
        elif x.getdiff() < target.getdiff():
            target = x
    # create list of stations with distance pairings near target
    dl = DistList(priority)
    dl.fill(stations, target)
    dlist = dl.distList

    if stations_has_rr_user(stations) is False: # if no stations with reroutable users then the algorithm stops
        return

    # ASSIGN STATION TO REROUTE FROM if priority is smaller than others and station has incoming users that can be rerouted
    rr = None
    for y in dlist:
        if y.station.has_rr_user() is True:  # checks if the station has an incoming reroutable user, skips otherwise
            if y.station.getdiff() > target.getdiff():  # checks if the differences are the same, if so it skips
                if rr is None:  # if not already assigned then assign
                    rr = y
                elif (y.priority > rr.priority) and priority != 3:  # choose the highest priority station
                    rr = y
                elif (y.priority < rr.priority) and priority == 3:  # if priority is only_distance choose lowest instead
                    rr = y

    # if there are no stations to take reroutable users from, i.e. target station has the only ones, stop algorithm
    if (rr is None):
        print('rr is None')
        return
    rr_station = rr.station  # assign rerouted station from distance pairings
    rr_user = rr_station.get_rr_user()  # get incoming user to reroute to target station

    # reroute user to target station(remove+append), mark them rerouted and increment k
    rr_station.inc.remove(rr_user)
    target.inc.append(rr_user)
    rr_user.rr_end = target
    rr_user.rerouted = True


def distribute(stations, priority, dist_constraint=False):
    target = get_target_station(stations)  # get target station
    # create list of stations with distance pairings near target
    dl = DistList(priority)
    dl.fill(stations, target)
    dlist = dl.distList

    if stations_has_rr_user(stations) is False: # if no stations with reroutable users then the algorithm stops
        return

    if dist_constraint is False:
        dist_constraint = 1000000000
    rrst = get_reroute_station(dlist, target, dist_constraint)  # assign reroute station for target station
    if rrst is None:
        return 0
    reroute_user(target, rrst)  # reroute user


def get_target_station(stations):  # grabs the station with the highest |difference| to be our target station
    target = None
    for x in stations:
        if target is None:
            if x.is_surplus() and x.has_rr_user():  # if the target has a surplus, must have a rr user to be target
                target = x
            elif x.is_deficit():
                target = x
        elif x.getdiff(absval=True) > target.getdiff(absval=True):  # set new target if |diff| is larger than curr
            if x.is_surplus() and x.has_rr_user():  # if the target has a surplus, must have a rr user to be target
                target = x
            elif x.is_deficit():
                target = x
    return target


def get_reroute_station(dlist, target, distance_constraint):  # gets rr station for target station
    rr = None
    if target.is_deficit():  # when target station has a deficit, get rrst to reroute user to target
        for y in dlist:
            s = y.station
            if s.has_rr_user():  # check to make sure station has a rerouteable user
                if (s.getdiff() > target.getdiff()) and s.is_surplus() and (y.dist < distance_constraint):
                    if rr is None:
                        rr = y
                    # this is where different priority checks would be placed
                    elif y.priority > rr.priority:  # if iterations priority > best so far, set as new best
                        rr = y
        if rr is None:
            print('Cannot distribute as no station meets the distance constraint')
            return None
        else:
            return rr.station
    elif target.is_surplus():  # when target station has a surplus, get rrst to reroute user from target
        for y in dlist:
            s = y.station
            if (s.getdiff() < target.getdiff()) and s.is_deficit() and (y.dist < distance_constraint):  # diff must be less than target diff
                if rr is None:
                    rr = y
                # this is where different priority checks would be placed
                elif y.priority < rr.priority:  # if iterations priority > best so far, set as new best
                    rr = y
        if rr is None:
            print('Cannot distribute as no station meets the distance constraint')
            return
        else:
            return rr.station


def reroute_user(target, rrst):  # reroutes user from (frm) one station to another (to)
    if target.is_deficit():  # when target station has a deficit, get rrst to reroute user to target
        to = target
        frm = rrst
    elif target.is_surplus():  # when target station has a surplus, get rrst to reroute user from target
        to = rrst
        frm = target

    user = frm.get_rr_user()  # get incoming user to reroute
    # reroute user to target station(remove+append) then mark them rerouted
    frm.inc.remove(user)
    to.inc.append(user)
    user.rr_end = to
    user.rerouted = True


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

