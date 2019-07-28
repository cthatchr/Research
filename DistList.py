from geopy import distance
from Station import *
from User import *
from StationDW import *
# given a station return a list of station with corresponding distance to station

class DistList:
    def __init__(self, priority):
        self.distList = []
        self.priority_used = priority

    # fills with a list of stations and their distance + priority to the target station
    def fill(self, stations, target):
        length = len(stations)
        targetLoc = (target.lat, target.lon)
        for x in range(length):  # creates a list excluding the target station
            if stations[x] != target:
                loc = (stations[x].lat, stations[x].lon)
                dist = distance.distance(loc, targetLoc).meters
                y = StationDW(stations[x], dist)
                self.distList.append(y)
        self.changePriority(self.priority_used)  # uses priority specified
        # self.distList.sort(key=lambda StationDW: StationDW.dist)  # sort

    # filter out stations outside the radius
    def distFilter(self, radius):
        flist = self.distList
        length = len(flist)
        for x in range(length):
            if flist[x].dist > radius:
                del flist[x:length]
                break
        return flist

    def printList(self):
        for x in range(len(self.distList)):
            print('Station: ' + self.distList[x].station.id, 'Distance: ' + str(self.distList[x].dist), 'Priority: ' + str(self.distList[x].priority))

    def distlist_has_rr_user(self):
        check = False
        for x in self.distList:
            if x.station.has_rr_user():
               check = True
        return check

    def changePriority(self, p):  # changes priority of all pairings to distance priority
        if p == 0:      # 0 = default    diff/dist
            for x in self.distList:
                x.default_priority()
        elif p == 1:    # 1 = dist prio  diff/dist^2
            for x in self.distList:
                x.distance_priority()
        elif p == 2:    # 2 = diff prio  diff^2/dist
            for x in self.distList:
                x.difference_priority()
        elif p == 3:     # 3 = only dist  dist
            for x in self.distList:
                x.only_distance()
        elif p == 4:    # 4 = only diff  diff
            for x in self.distList:
                x.only_difference()
        elif p == 5:    # 5 = random    rand(0, len)
            rand = list(range(0, len(self.distList)))
            random.shuffle(rand)
            for x in self.distList:
                x.priority = rand.pop()
