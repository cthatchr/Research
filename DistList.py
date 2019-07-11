from geopy import distance
from Station import *
from User import *
from StationDW import *
# given a station return a list of station with corresponding distance to station

class DistList:
    def __init__(self):
        self.distList = []

    # fills dict with the list of stations and their distance to the target station
    def distFill(self, stations, target):
        length = len(stations)
        targetLoc = (target.lat, target.lon)
        for x in range(length):
            # creates a list excluding the target station
            if stations[x] != target:
                loc = (stations[x].lat, stations[x].lon)
                dist = distance.distance(loc, targetLoc).meters
                y = StationDW(stations[x], dist)
                self.distList.append(y)
        # sort
        self.distList.sort(key=lambda StationDW: StationDW.dist)
        # delete first one which is the target station
        # self.distList.pop(0)



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