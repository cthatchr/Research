from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *


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

