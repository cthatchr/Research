import random

class User:
    def __init__(self, id='U', start=0, dest=0, rerouted = False):
        self.id = id #id, u1..
        self.start = start #start station
        self.dest = dest #destination station
        self.rerouted = rerouted # marks if a user was already rerouted

    def createRandUser(self, stations):
        # assign random id if not given
        if self.id == 'U':
            self.id = 'U%03x' % random.randrange(16 ** 3)

        randstart = random.randint(0, len(stations)-1)
        randdest = random.randint(0, len(stations)-1)
        # if start and dest are the same re roll until not the same
        while randstart == randdest:
            randstart = random.randint(0, len(stations)-1)
            randdest = random.randint(0, len(stations)-1)

        self.start = stations[randstart]
        self.dest = stations[randdest]
        self.rerouted = False

        # add user to incoming for station
        # print(self)
        self.dest.inc.append(self)

    def printuser(self):
        return 'ID: ' + self.id, 'Start: ' + self.start.id, 'Destination: ' + self.dest.id


def createUsers(stations, amount):
    users = []
    # print("Creating", amount, 'users.')
    for x in range(amount):
        id = 'U' + str(x + 1)
        # create user
        u = User(id=id)
        u.createRandUser(stations)
        users.append(u)
    return users
