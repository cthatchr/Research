from geopy import distance
# Add all current stock from stations
# Divide by number of stations, save value as target amount for each
# If curr stock > target amt, remove incoming to pool
# If curr stock < target amt, add from pool

#creates an even distribution of bikes
def even_dist(stations):
    total = 0
    pool = []
    # finds total amount of bikes that will be in these stations so we can find the target amt(total/#stations
    for x in stations:
        total += x.curr
        total += len(x.inc)
    target = total/len(stations)
    print("Even distribution target for each station is: ", round(target))
    # goes through list of stations and checks the ones who have too many in stock
    # adding them to the extra pool to be redistribted
    for x in stations:
        st = x.curr + len(x.inc)
        # if current stock is already > target
        if x.curr > target:
            print(x.id + " has a surplus of stock.", int(st - target))
            for y in range(len(x.inc)):
                i = len(x.inc) - 1
                pool.append(x.inc[i])
                x.inc.pop()
                print(pool[len(pool) - 1].id + " moved to pool to be rerouted")
        # base case
        elif st > target:
            print(x.id + " has a surplus of stock.", int(st-target))
            for y in range(int(st-target)):
                i = len(x.inc)-1
                pool.append(x.inc[i])
                x.inc.pop()
                print(pool[len(pool)-1].id + " moved to pool to be rerouted")
    # goes through stations and checks the ones who have too little in stock
    # reroutes users in the pool to these stations
    for x in stations:
        st = x.curr + len(x.inc)
        # if there isn't enough, put the rest into the last
        if len(pool) < target-st:
            print(x.id + " has insufficient stock.", int(target - st))
            for y in range(len(pool)):
                i = len(pool) - 1
                x.inc.append(pool[i])
                pool.pop()
                print(x.inc[len(x.inc)-1].id + " rerouted from pool.")
        elif st < target: # if incoming amount will put you below target
            print(x.id + " has insufficient stock.", int(target-st))
            for y in range(int(target-st)):
                i = len(pool) - 1
                x.inc.append(pool[i])
                pool.pop()
                print(x.inc[len(x.inc)-1].id + " rerouted from pool.")
    for x in stations:
        print("Station " + x.id + " has " + str(x.curr) + " current stock and " + str(len(x.inc)) + " incoming stock, for a final stock of " + str(x.curr+len(x.inc)))


u1 = User("u1", 0, 0)
u2 = User("u2", 0, 0)
u3 = User("u3", 0, 0)
u4 = User("u4", 0, 0)
d1 = Station("d1", 10, 7, [u1,u3,u4])
d2 = Station("d2", 10, 3, [u2])
d3 = Station("d3", 10, 2, [])

stations = [d1,d2,d3]

even_dist(stations)