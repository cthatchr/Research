from Station import *
class StationDW:
    def __init__(self, station, dist):
        self.station = station  # station
        self.dist = dist  # distance to target station
        self.priority = (station.getdiff())/dist # priority in regards to target, default

    def default_priority(self):
        s = self.station
        self.priority = (s.target-s.curr)/self.dist

    def distance_priority(self):  # prioritizes distance when calculating priority, dist value is to the power of 2
        s = self.station
        self.priority = (s.target - s.curr) / pow(self.dist, 2)
