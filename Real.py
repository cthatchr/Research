from plots import *
from Station import *
from Algorithm import *

def set_real_settings(): # select settings for real data run
    settings = []
    choice = {}
    choice['1'] = "Low"
    choice['2'] = "Medium"
    choice['3'] = "High"
    choice['4'] = "Random"

    while True:
        try:
            settings.append((int(input
                                 ('A random date will be used. In minutes, how many user trips would you like to use?:'))))
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = int(input("Target Distribution:"))
        if 1 <= selection <= 4:
            settings.append(selection)
            break
        else:
            print('select again')

    stations = load_stations()  # loads stations with specific target distribution
    set_stations_t_distr(stations, settings[1])  # sets target distribution for stations
    users = load_users_time(stations, settings[0])

    compare_real(stations, users)
    # run_real(settings)


def run_real(stations, users,  p):  # runs with real dataset

    sum = StationsDiff(stations)  # get sum of stations difference in stock before run
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    avg = sum / len(stations)  # avg difference, per run

    stats_sum = [sum]
    stats_avg = [avg]
    stats_dist = [dist_rr]

    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            distribute_single(stations, p)  # runs algorithm, rerouting a single user then recording data
        else:
            print('stations MEET targets')

        sum = StationsDiff(stations)  # get sum of stations difference in stock
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        avg = sum / len(stations)  # avg difference, per run

        stats_sum.append(sum)
        stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_sum, stats_avg, stats_dist]


def compare_real(stations, users):  # runs and compares real data against the different priority options
    stats_sum = []
    stats_avg = []
    stats_dist = []
    index = np.arange(len(users)+1)

    for x in range(6):  # runs algorithm with different prio, starts fresh each time
        stats = run_real(stations, users, x)  # run alg and gather data for priority x
        stats_sum.append(stats[0])  # fill data into arrays to use to create plots
        stats_avg.append(stats[1])
        stats_dist.append(stats[2])
        reset_users(users)  # reset users back to original positions

    stats_sum = np.array(stats_sum)
    stats_avg = np.array(stats_avg)
    stats_dist = np.array(stats_dist)

    # print(stats_dist)
    compare_lineplot(index, stats_sum, stats_avg, stats_dist)  # create plot here