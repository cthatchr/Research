import matplotlib.pyplot as plt
from plots import *
from Algorithm import *


def curr_settings():  # current build for testing purposes
    settings = []
    choice = {}
    choice['1'] = "Distance Constraint(Average Distance)"
    choice['2'] = "No Distance Constraint"
    choice['3'] = "Compare Both"

    while True:
        try:
            settings.append((int(input('How many users would you like to create and reroute?:'))))
            break
        except:
            print('Enter an integer.')

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':  # with a distance constraint
            settings.append(True)
            compare_curr(settings)
            break
        elif selection == '2':  # no distance constraint
            settings.append(False)
            compare_curr(settings)
            break
        elif selection == '3':  # compare run with and without a distance constraint
            settings.append('Both')
            compare_curr_both(settings)
            break
        else:
            print('select again')
    plt.show()


def run_curr(stations, users, p, constraint):
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted

    stats_dist = [dist_rr]

    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            passed = distribute(stations, p, constraint)  # runs algorithm, rerouting a single user then recording data
            if passed is 0:
                return 0
        else:
            print('stations MEET targets')
        # sum = StationsDiff(stations)  # get sum of stations difference in stock
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
        # avg = sum / len(stations)  # avg difference, per run

        # stats_sum.append(sum)
        # stats_avg.append(avg)
        stats_dist.append(dist_rr)

    return [stats_dist]


def compare_curr(settings, k=5):
    j = 0
    failed = False
    t = (39.953555, -75.164042)
    amt_users = settings[0]+1
    stats_dist = np.array([[0] * amt_users] * 6)
    index = np.arange(amt_users)

    while j < k:  # run algorithm k times

        stations = load_stations()  # loads stations, their target = curr
        filter_stations(stations, 1000, t)  # filters out farther stations
        variance = create_sd_dist(settings[0],
                                  stations)  # figure out stations target(i.e. their surplus and deficit)
        users = dist_users(variance, stations)

        if settings[1] is True:
            constraint = get_average_distance(stations)*1.5
        else:
            constraint = False

        temp_stats = np.array([[0] * amt_users] * 6)

        for x in range(6):  # runs algorithm with different prio, starts fresh each time
            stats = run_curr(stations, users, x, constraint)  # run alg and gather data for priority x with constraint
            if stats is 0:  # if instance fails stop and make a new one
                print('Failed on priority #',x,'. Creating new instance')
                failed = True
                break
            else:  # else keep going
                temp_stats[x] = np.add(temp_stats[x], stats)
                reset_users(users)  # reset users back to original positions
                failed = False

        if failed is False:
            stats_dist = np.add(stats_dist, temp_stats)
            j += 1
            print('Found passing instance #', j)

        delete_inc(stations)  # clear users from stations

    stats_dist = stats_dist / k

    create_dist_plot(index, stats_dist)  # create plot here


def compare_curr_both(settings, k=5):
    j = 0
    failed = False
    t = (39.953555, -75.164042)
    amt_users = settings[0] + 1
    stats_dist_constraint = np.array([[0] * amt_users] * 6)  # initialize stat arrays
    stats_dist = np.array([[0] * amt_users] * 6)
    index = np.arange(amt_users)

    while j < k:  # run algorithm k times

        stations = load_stations()  # loads stations, their target = curr
        filter_stations(stations, 1000, t)  # filters out farther stations
        variance = create_sd_dist(settings[0],
                                  stations)  # figure out stations target(i.e. their surplus and deficit)
        users = dist_users(variance, stations)
        constraint = get_average_distance(stations) * 1.5

        temp_constraint = np.array([[0] * amt_users] * 6)  # initialize stat arrays
        temp_stats = np.array([[0] * amt_users] * 6)

        for x in range(6):  # runs algorithm with different prio, starts fresh each time
            stats = run_curr(stations, users, x, False)  # run alg and gather data for priority x without constraint
            temp_stats[x] = np.add(temp_stats[x], stats)  # record instance data
            reset_users(users)  # reset users back to original positio

            stats = run_curr(stations, users, x, constraint)  # run alg and gather data for priority x with constraint
            if stats is 0:  # if instance fails stop and make a new one
                print('Failed on priority #', x, '. Creating new instance')
                failed = True
                break
            else:
                temp_constraint[x] = np.add(temp_constraint[x], stats)  # record instance data
                reset_users(users)  # reset users back to original positions
                failed = False

        if failed is False:
            stats_dist = np.add(stats_dist, temp_stats)
            stats_dist_constraint = np.add(stats_dist_constraint, temp_constraint)
            j += 1
            print('Found passing instance #', j)

        delete_inc(stations)  # clear users from stations

    stats_dist = stats_dist / k
    stats_dist_constraint = stats_dist_constraint / k

    create_dist_plot(index, stats_dist)  # create plot without constraint
    create_dist_plot(index, stats_dist_constraint)  # create plot with constraint


def compare_curr_single(stations, users, constraint):
    stats_dist = []
    index = np.arange(len(users) + 1)

    for x in range(6):  # runs algorithm with different prio, starts fresh each time
        stats = run_curr(stations, users, x, constraint)  # run alg and gather data for priority x with constraint
        if stats is 0:
            print('Cannot distribute due to distance constraint')
            return
        # stats_sum[x] = np.add(stats_sum[x], stats[0])  # record instance data
        # stats_avg[x] = np.add(stats_avg[x], stats[1])
        stats_dist[x] = np.add(stats_dist[x], stats)
        reset_users(users)  # reset users back to original positions

    delete_inc(stations)  # clear users from stations

    create_dist_plot(index, stats_dist)  # create plot here