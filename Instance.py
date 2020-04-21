
class Instance:
    def __init__(self, stations, users):
        self.stations = stations
        self.users = users
        self.priority0_pass = 9
        self.priority1_pass = 9
        self.priority2_pass = 9
        self.priority3_pass = 9

    def update_priority_pass(self, priority, constraint):
        if priority is 0:
            self.priority0_pass = constraint
        elif priority is 1:
            self.priority1_pass = constraint
        elif priority is 2:
            self.priority2_pass = constraint
        elif priority is 3:
            self.priority3_pass = constraint