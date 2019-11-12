import matplotlib.pyplot as plt
from plots import *
from Algorithm import *
from Flow_Algorithm import *


def choose_settings():
    settings = []
    choice2 = {}
    choice2['1'] = "Distance Constraint(Average Distance)"
    choice2['2'] = "No Distance Constraint"
    choice2['3'] = "Compare Both"
    choice = {}
    choice['1'] = "Normal"
    choice['2'] = "Uniform"
    choice['3'] = "Exponential"
    choice['4'] = "Random"

    while True:  # 0
        try:
            settings.append((int(input('How many users would you like to create and reroute?:'))))
            break
        except:
            print('Enter an integer.')

    while True:  # 1
        try:
            settings.append((int(input('How many times would you like it to be run?:'))))
            break
        except:
            print('Enter an integer.')

    while True:  # 2
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':
            settings.append('N')
            break
        elif selection == '2':
            settings.append('U')
            break
        elif selection == '3':
            settings.append('E')
            break
        elif selection == '4':
            settings.append('R')
            break
        else:
            print('select again')

    while True:
        options = choice2.keys()
        for x in options:
            print(x, choice2[x])

        selection = input("Select:")
        if selection == '1':  # with a distance constraint

            while True:  # 3
                try:
                    settings.append([False, (float(
                        input('constraint = average distance between stations * x. What should x = ?(i.e. 1.5):')))])
                    break
                except:
                    print('Enter a float.')
            break
        elif selection == '2':  # no distance constraint
            settings.append([False, False])  # 3
            break
        elif selection == '3':  # compare run with and without a distance constraint
            while True:  # 3
                try:
                    settings.append([True, (float(
                        input('constraint = average distance between stations * x. What should x = ?(i.e. 1.5):')))])
                    break
                except:
                    print('Enter a float.')
            break
        else:
            print('select again')
    return settings


def run(settings, type):
    j = 0
    k = settings[1]
    mcf_stats = [0] * k
    greedy_stats = [0] * k

    if type is 'G':  # if greedy
        while j < k:
            data = create_data(settings)
            stats = run_greedy(settings, data[0], data[1])  # returns [stats, const_stats]

            if stats is not 0:
                greedy_stats[j] = stats
                j += 1
            delete_inc(data[0])
        return greedy_stats

    elif type is 'M':  # if mcf
        while j < k:
            data = create_data(settings)
            stats = run_mcf(settings, data[0], data[1])  # returns [stats, const_stats]
            if stats is not 0:
                mcf_stats[j] = stats
                j += 1
            delete_inc(data[0])
        # print(mcf_stats)
        return mcf_stats

    elif type is 'B':  # if running both
        while j < k:
            data = create_data(settings)
            stats_m = run_mcf(settings, data[0], data[1])  # returns [stats, const_stats]
            stats_g = run_greedy(settings, data[0], data[1])  # returns [stats, const_stats]
            if (stats_m is not 0) and (stats_g is not 0):
                mcf_stats[j] = stats_m  # returns [stats, const_stats]
                greedy_stats[j] = stats_g  # returns [stats, const_stats]
                j += 1
                print('Completed run', j)
            delete_inc(data[0])
        # print('MCF', mcf_stats)
        # print('Greedy', greedy_stats)
        return [mcf_stats, greedy_stats]


def create_data(settings):
    stations = load_stations()  # loads stations, their target = curr
    # filter_stations(stations, 1000, (39.953555, -75.164042))  # filters out farther stations
    variance = sd_dist(settings[0],
                                  stations, settings[2])  # figure out stations target(i.e. their surplus and deficit)
    users = dist_users(variance, stations)

    return[stations, users]


def run_mcf(settings, stations, users):

    failed = 0
    stats_constraint = 0

    if settings[3][0] is False:
        if settings[3][1] is False:
            constraint = False
        else:
            constraint = get_average_distance(stations) * settings[3][1]

        stats = min_cost_alg(stations, users, constraint)  # run alg and gather data for priority x with constraint
        if stats is 0:  # if instance fails stop and make a new one
            print('Failed. Creating new instance')
        else:  # else keep going
            return stats

    elif settings[3][0] is True:
            stats = min_cost_alg(stations, users, False)  # run alg and gather data without constraint
            constraint = get_average_distance(stations) * settings[3][1]
            stats_const = min_cost_alg(stations, users,
                                      constraint)  # run alg and gather data for priority x with constraint

            if stats_const is 0:  # if instance fails stop and make a new one
                print('Failed instance.')
            else:  # else keep going
                return [stats, stats_const]


def run_greedy(settings, stations, users):

    failed = False
    amt_users = settings[0] + 1
    stats_const = np.array([[0] * amt_users] * 4)
    stats = np.array([[0] * amt_users] * 4)

    if settings[3][0] is False:  # if running eithe with or without constraint

        if settings[3][1] is False:
            constraint = False
        else:
            constraint = get_average_distance(stations) * settings[3][1]

        for x in range(4):  # runs algorithm with different prio, starts fresh each time
            temp = run_priority(stations, users, x,
                                constraint)  # run alg and gather data for priority x with constraint

            if temp is 0:  # if instance fails stop and make a new one
                print('Failed on priority #', x, '. Creating new instance')
                failed = True
                break
            else:  # else keep going
                stats[x] = np.add(stats[x], temp)
                reset_instance(users, stations)  # reset users back to original positions
                failed = False

        if failed is False:
            print('Passing instance')
            return stats
        else:
            return 0

    elif settings[3][0] is True:
        constraint = get_average_distance(stations) * settings[3][1]
        for x in range(4):  # runs algorithm with different prio, starts fresh each time
            temp = run_priority(stations, users, x, False)  # run alg and gather data for priority x with constraint
            reset_instance(users, stations)  # reset users back to original position
            temp_const = run_priority(stations, users, x, constraint)  # priority x with constraint

            if temp_const is 0:  # if instance fails stop and make a new one
                print('Failed on priority #', x, '. Creating new instance')
                failed = True
                break
            else:  # else keep going
                stats[x] = np.add(stats[x], temp)
                stats_const[x] = np.add(stats_const[x], temp_const)
                reset_instance(users, stations)  # reset users back to original positions
                failed = False

        if failed is False:
            print('Passing instance')
            return [stats, stats_const]
        else:
            return 0


def run_priority(stations, users, p, constraint):  # run the greedy algorithm for a specific priority type
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    stats_dist = [dist_rr]

    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            passed = distribute(stations, p, constraint)  # runs algorithm, rerouting a single user then recording data
            if passed is 0:
                return 0
        else:
            print('stations MEET targets')
        dist_rr = total_RR_distance(users)  # get the total distance users were rerouted

        stats_dist.append(dist_rr)

    return [stats_dist]


def greedy_average(stats):
    total = stats[0]
    for x in range(1, len(stats)):
        total = np.add(total, stats[x])

    avg = total/len(stats)
    # print(avg)
    return avg


def greedy_lowest_dist(stats):
    best = None
    for x in range(len(stats)):
        if (best is None) or best > stats[x][-1]:
            best = stats[x][-1]
            priority = x
    return [best, priority]


def mcf_average(stats):
    total = sum(stats)

    avg = total/len(stats)
    # print(avg)
    return avg


def reset_instance(users, stations):  # resets the users so we can run the algorithm fresh
    for x in users:
        if x.rr_end is not None:  # resets as long as user was rerouted
            x.rr_end.inc.remove(x)  # remove user from rerouted stations incoming
            x.rr_end = None  # reset users rerouted station
            x.end.inc.append(x)  # add user back to original stations incoming
            x.rerouted = False
