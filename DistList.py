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

    def fill_distance(self, stations, target):
        length = len(stations)
        targetLoc = (target.lat, target.lon)
        for x in range(length):  # creates a list excluding the target station
            if stations[x] != target:
                loc = (stations[x].lat, stations[x].lon)
                dist = distance.distance(loc, targetLoc).meters
                y = StationDW(stations[x], dist)
                self.distList.append(y)

    def changePriority(self, p):  # changes priority of all pairings to distance priority
        if p == 0:      # 0 = default    diff/dist
            for x in self.distList:
                x.distance_priority()
        elif p == 1:    # 1 = dist prio  diff/dist^2
            for x in self.distList:
                x.difference_priority()
        elif p == 2:    # 2 = diff prio  diff^2/dist
            for x in self.distList:
                x.only_distance()
        elif p == 3:     # 3 = only dist  dist
            rand = list(range(0, len(self.distList)))
            random.shuffle(rand)
            for x in self.distList:
                x.priority = rand.pop()

    def changePriority_deprecated(self, p):  # changes priority of all pairings to distance priority
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