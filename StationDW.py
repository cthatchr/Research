from Station import *
class StationDW:
    def __init__(self, station, dist):
        self.station = station  # station
        self.dist = dist  # distance to target station
        self.priority = (station.getdiff())/dist # priority in regards to target

    def setPrio(self):
        s = self.station
        self.priority = (s.target-s.curr)/self.dist
