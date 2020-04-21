from Station import *
class StationDW:
    def __init__(self, station, dist):
        self.station = station  # station
        self.dist = dist  # distance to target station
        self.priority = 0 # (station.getdiff())/dist  # priority in regards to target, default

    def default_priority(self):
        s = self.station
        self.priority = s.getdiff(absval=True)/self.dist

    def distance_priority(self):  # prioritizes distance when calculating priority, dist value is to the power of 2
        s = self.station
        self.priority = s.getdiff(absval=True) / pow(self.dist, 2)

    def difference_priority(self):  # prioritizes difference when calculating priority, diff to the power of 2
        s = self.station
        self.priority = pow(s.getdiff(absval=True), 2) / self.dist

        '''if s.is_surplus_or_deficit is -1:  # if the station has a deficit set the priority to negative
            self.priority = -self.priority'''

    def only_distance(self):  # priority becomes the distance between stations, lowest
        self.priority = self.dist

    def only_difference(self):  # priority becomes the difference, highest
        self.priority = self.station.getdiff()

    def random_priority(self, prio):  # assign random order in which stations are prioritized
        self.priority = prio