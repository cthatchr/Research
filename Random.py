from plots import *
from Station import *
from Algorithm import *

def set_rand_settings():
    settings = []
    choice = {}
    choice['1'] = "Low"
    choice['2'] = "Medium"
    choice['3'] = "High"
    choice['4'] = "Random"

    # select settings
    """while True:
        try:
            settings.append((int(input('How many stations would you like to create?:'))))  # 0
            break
        except:
            print('Enter an integer.')"""

    settings.append(1)
    while True:
        try:
            settings.append(int(input('How many incoming users would you like to create?:')))  # 1
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('How many incoming users are we allowed to move?:')))  # 2
            break
        except:
            print('Enter an integer.')

    while True:
        try:
            settings.append(int(input('Number of tests per run?:')))  # 3
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Target Distribution:"))  # 4
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Current Distribution:"))  # 5
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    stations = load_stations()  # create an instance of stations with curr/target amt
    compare_random(stations, settings)


def run_random(stations, users, settings, p):  # runs with same random data

    sum = StationsDiff(stations)  # get sum of stations difference in stock before run
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    avg = sum / len(stations)  # avg difference rerouted

    stats_sum = [sum]
    stats_avg = [avg]
    stats_dist = [dist_rr]

    for k in range(settings[2]):  # users allowed to move

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            distribute_single(stations, p)  # runs algorithm, rerouting a single user then recording data
        else:
            print('stations MEET targets')

        sum = StationsDiff(stations)  # get sum of stations difference in stock before, per run
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_sum, stats_avg, stats_dist]  # return instance j's stats for priority x


def compare_random(stations, settings):
    stats_sum = np.array([[0]*(settings[1]+1)]*6)  # initialize stat arrays
    stats_avg = np.array([[0]*(settings[1]+1)]*6)
    stats_dist = np.array([[0]*(settings[1]+1)]*6)
    index = np.arange(settings[1]+1)

    for j in range(settings[3]):  # run algorithm j times, i.e 50
        set_stations_t_distr(stations, settings[4])  # reset the target distribution
        set_stations_c_distr(stations, settings[5])  # reset the current distribution
        delete_inc(stations)  # clear users from stations
        users = create_rand_users(stations, settings[1])  # create random incoming users to stations

        for x in range(6):  # runs algorithm with different priority, starts fresh each time
            reset_users(users)  # reset users back to original positions
            stats = run_random(stations, users, settings, x)  # run alg and gather data for priority x

            stats_sum[x] = np.add(stats_sum[x], stats[0])  # record instance data
            stats_avg[x] = np.add(stats_avg[x], stats[1])
            stats_dist[x] = np.add(stats_dist[x], stats[2])

    delete_inc(stations)  # clear users from stations

    stats_sum = stats_sum / settings[3]
    stats_avg = stats_avg / settings[3]
    stats_dist = stats_dist / settings[3]

    compare_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here