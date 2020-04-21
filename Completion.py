import matplotlib.pyplot as plt
import math
from plots import *
from Algorithm import *
import copy
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


def run_consistent(settings, reroutes, stations, users):
    f = open("currData.txt", "a+")
    j = 0
    failed = 0
    skip = 0
    k = settings[1]
    mcf_stats = [0] * k
    greedy_stats = [0] * k
    totalfails = 0

    while j < k:
        data = create_data(settings)
        stats_m = run_mcf(settings, data[0], data[1], reroutes)  # returns [stats, const_stats]
        print(stats_m)
        stats_g = run_greedy(settings, data[0], data[1])  # returns [stats, const_stats]
        print(stats_g)
        if (stats_m is not 0) and (stats_g is not 0):
            failed = 0
            mcf_stats[j] = stats_m[1]  # returns [stats, const_stats]
            greedy_stats[j] = stats_g  # returns [stats, const_stats]
            j += 1
            print('Completed run', j)
            print('Completed run', j, file=f)
            # print('Greedy(Diff/Dist^2, Diff^2/Dist, Only Dist, Random):\n', stats_g)
            # print('MCF:\n', stats_m[1])
        else:
            failed += 1
            totalfails += 1
            if (failed == 15):
                return 0
        delete_inc(data[0])

    print('# of fails:', totalfails)
    print('# of fails:', totalfails, file=f)
    f.close()
    return [mcf_stats, greedy_stats]


def run(settings, type):
    f = open("currData.txt", "a+")
    j = 0
    failed=0
    skip = 0
    k = settings[1]
    mcf_stats = [0] * k
    greedy_stats = [0] * k
    totalfails = 0

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
            if(stats_m is not 0) and (stats_g is not 0):
                failed = 0
                mcf_stats[j] = stats_m[1]  # returns [stats, const_stats]
                greedy_stats[j] = stats_g  # returns [stats, const_stats]
                j += 1
                print('Completed run', j)
                print('Completed run', j, file=f)
                # print('Greedy(Diff/Dist^2, Diff^2/Dist, Only Dist, Random):\n', stats_g)
                # print('MCF:\n', stats_m[1])
                '''
                else:
                skip += 1
                if skip is (2*k):
                    
               
                '''
            else:
                failed += 1
                totalfails += 1
                if(failed == 15):
                    return 0
            delete_inc(data[0])

        # print('Greedy', greedy_stats)
        # print('MCF', mcf_stats)
        print('# of fails:', totalfails)
        print('# of fails:', totalfails, file=f)
        f.close()
        return [mcf_stats, greedy_stats]


def create_data(settings):
    stations = load_stations()  # loads stations, their target = curr
    filter_stations(stations, 3000, (39.953555, -75.164042))  # filters out farther stations
    # print(len(stations))
    variance = sd_dist(settings[0],
                                  stations, settings[2])  # figure out stations target(i.e. their surplus and deficit)
    users = dist_users(variance, stations)

    return[stations, users]


def run_mcf(settings, stations, users, reroutes=False):

    failed = 0
    stats_constraint = 0

    if settings[3][0] is False:
        if settings[3][1] is False:
            constraint = False
        else:
            constraint = get_average_distance(stations) * settings[3][1]
        if reroutes is False:
            stats = min_cost_alg(stations, users, constraint, individual=True)  # run alg and gather data
        else:
            stats = min_cost_alg(stations, users, constraint, individual=True, reroutes=reroutes)  # run alg and gather data

        if stats is 0:  # if instance fails stop and make a new one
            print('MCF failed.')
            return 0
        else:  # else keep going
            return stats

    elif settings[3][0] is True:
            stats = min_cost_alg(stations, users, False)  # run alg and gather data without constraint
            constraint = get_average_distance(stations) * settings[3][1]
            stats_const = min_cost_alg(stations, users,
                                      constraint)  # run alg and gather data for priority x with constraint

            if stats_const is 0:  # if instance fails stop and make a new one
                print('MCF failed.')
            else:  # else keep going
                return [stats, stats_const]

def run_greedy2(settings, instance):
    passed = 0
    stations = instance.stations
    users = instance.users
    fails = [0,0,0,0]
    amt_users = settings[0]
    stats = np.array([[0] * amt_users] * 4)
    avg_dist = get_average_distance(stations)
    constraint = avg_dist * settings[3][1]
    print(get_average_distance(stations), constraint)

    for x in range(4):  # runs algorithm with different prio, starts fresh each time
        temp = run_priority(stations, users, x,
                            constraint)  # run alg and gather data for priority x with constraint

        if (x is 3) and (temp is 0):
            reset_instance(users, stations)
            if instance.priority3_pass < settings[3][1]:
                while temp is 0:
                    temp = run_priority(stations, users, x,
                                        constraint)  # run alg and gather data for priority x with constraint
                    reset_instance(users, stations)
            else:
                i = 0
                while temp is 0 and i < passed:
                    temp = run_priority(stations, users, x,
                                        constraint)  # run alg and gather data for priority x with constraint
                    reset_instance(users, stations)
                    i += 1

        if temp is 0:  # if instance fails stop and make a new one
            print('Greedy failed on priority #', x, '.')
            fails[x] = 1
            stats[x] = np.full(amt_users, avg_dist)
            reset_instance(users, stations)

        else:
            print('Greedy passed on priority #', x, '.')
            instance.update_priority_pass(x, settings[3][1])
            passed += 1
            stats[x] = temp
            reset_instance(users, stations)  # reset users back to original positions

    return stats, fails


def run_greedy(settings, stations, users):

    failed = False
    amt_users = settings[0]
    stats_const = np.array([[0] * amt_users] * 4)
    stats = np.array([[0] * amt_users] * 4)


    if settings[3][0] is False:  # if running eithe with or without constraint

        if settings[3][1] is False:
            constraint = False
        else:
            constraint = get_average_distance(stations) * settings[3][1]
            print(get_average_distance(stations), constraint)

        for x in range(4):  # runs algorithm with different prio, starts fresh each time
            temp = run_priority(stations, users, x,
                                constraint)  # run alg and gather data for priority x with constraint

            if (x is 3) and (temp is 0):
                reset_instance(users, stations)
                while temp is 0:
                    temp = run_priority(stations, users, x,
                                        constraint)  # run alg and gather data for priority x with constraint
                    reset_instance(users, stations)

            if temp is 0:  # if instance fails stop and make a new one
                print('Greedy failed on priority #', x, '.')
                failed = True
                reset_instance(users, stations)
                break
            else:  # else keep going
                stats[x] = temp
                reset_instance(users, stations)  # reset users back to original positions
                failed = False

        if failed is False:
            # print('Passing instance')
            # print(stats)
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
                print('Greedy failed on priority #', x, '.')
                failed = True
                reset_instance(users, stations)
                break
            else:  # else keep going
                stats[x] = np.add(stats[x], temp)
                stats_const[x] = np.add(stats_const[x], temp_const)
                reset_instance(users, stations)  # reset users back to original positions
                failed = False

        if failed is False:
            # print('Passing instance')
            return [stats, stats_const]
        else:
            return 0


def run_priority(stations, users, p, constraint):  # run the greedy algorithm for a specific priority type
    dist_rr = total_RR_distance(users)  # get the total distance users were rerouted
    stats_dist = []
    prev = dist_rr
    for k in range(len(users)):  # run with real data

        if meetsTarget(stations) is False:  # run distribution if stations don't meet targets
            passed = distribute(stations, p, constraint)  # runs algorithm, rerouting a single user then recording data
            if passed is 0:
                return 0
        else:
            print('stations MEET targets')
        rr_dist = total_RR_distance(users)
        dist_rr = rr_dist - prev  # get the total distance users were rerouted
        prev = rr_dist

        stats_dist.append(dist_rr)

    return np.array(stats_dist)


def greedy_average(stats):
    total = stats[0]
    # print(stats[0])
    for x in range(1, len(stats)):
        total = np.add(total, stats[x])

    avg = total/len(stats)
    # print(avg)
    return avg


def greedy_indv(stats):
    # temp = stats.copy()
    for x in stats:
        prev = x[1]
        # print(x)
        for y in range(2, len(x)):
            # print(x[y])
            x[y] = x[y] - prev
            prev += x[y]

    return stats


def greedy_lowest_dist(stats):
    best = None
    for x in range(len(stats)):
        if (best is None) or best > stats[x][-1]:
            best = stats[x][-1]
            priority = x
    return [best, priority]


def mcf_total(stats):
    total = []
    for x in stats:
        temp = sum(x)
        total.append(temp)
    return total


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


def cost_function(stats, type):
    if type is 'power':
        return np.array([((x ** 2)/1000) for x in stats])
    elif type is 'step':
        return [((x//1000)*100) for x in stats]


def clean(stats):
    # first change each array to the individual values, then change to the cost function, then get average and sum
    # first array is the settings for the users run
    # print(stats)
    for x in stats:
        # second array is the runs for the settings
        for y in x:
            # third array is the priorities for each run
            if y is not 0:
                if y[0] is type(0):
                    print(x)
                    temp_stats = greedy_indv(x)
                else:
                    print(y)
                    temp_stats = greedy_indv(y)
            '''for z in y:
                # print(z)
                # fourth array is the data for each priority'''
    print(stats)


def big_tolist(stats):
    # print('IN TOLIST')
    # print(stats)

    for x in range(len(stats)):
        # print('X')
        # print(type(stats[x]))
        # print(type(np.array([0])))
        if type(stats[x]) is type(np.array([0])):
            # print('IS NP')
            stats[x] = stats[x].tolist()
            for y in range(len(stats[x])):
                # print('Y')
                if type(stats[x][y]) is type(np.array([0])):
                    # print('IS NP')
                    stats[x][y] = stats[x][y].tolist()
        elif type(stats[x]) is type([0]):
            for y in range(len(stats[x])):
                # print('Y')
                # print(type(stats[x][y]))
                if type(stats[x][y]) is type(np.array([0])):
                    # print('IS NP')
                    stats[x][y] = stats[x][y].tolist()
                elif type(stats[x][y]) is type(0):
                    continue
    print('Done with tolist')



def create_cost(stats, function, type):  # create new list based on cost function
    cost_stats = copy.deepcopy(stats)
    print(cost_stats)
    if type is 'g':
        for x in range(len(cost_stats)):
            print(cost_stats[x])
            if cost_stats[x][0] == 0:
                continue
            for y in range(len(cost_stats[x])):
                print(cost_stats[x][y])
                cost_stats[x][y] = cost_function(cost_stats[x][y], function)
        return cost_stats

    elif type is 'm':
        print('m')
        print(cost_stats)
        for x in range(len(cost_stats)):
            print(cost_stats[x])
            cost_stats[x] = cost_function(cost_stats[x], function)
        return cost_stats


def avg_dist(stats, type):
    if type is 'g':
        avgs = []

        for x in range(len(stats)):
            temp = stats[x][0]
            # print('0', temp)
            if temp is 0:
                avgs.append([0, 0, 0, 0])
                continue
            else:
                tempz = [0, 0, 0, 0]
                for z in range(len(stats[x])):
                    tempz[z] = np.sum(stats[x][z]) / (len(stats[x][z])-1)
                avgs.append(tempz)
            # print(tempz)
        return avgs
    elif type is 'm':
        avgs = []
        for x in range(len(stats)):
            temp = np.sum(stats[x]) / (len(stats[x]))
            avgs.append(temp)
            # print(tempz)
        return avgs

def users_avg_runs(stats, type):
    if type is 'g':
        avgs = []  # len(stats[-1][0])] number of runs
        # print(avgs)
        # print(stats)
        temp = 0
        for x in range(len(stats)):  # run data
            # print(len(stats))
            temp = np.add(temp, stats[x])
            print('0', temp)
            # print(y, stats[x][y])
            # print(temp)

            # print(avgs)'

        temp = np.true_divide(temp, len(stats))
        return temp.tolist()
    elif type is 'm':
        # print('mcf')
        avgs = []
        # print(avgs)
        for x in range(len(stats)):  # run data
            # print('x')
            temp = stats[x][0]
            # print('0', temp)
            if temp is 0:
                avgs.append([0])
                continue
            for y in range(1, len(stats[x])):  #
                # print(y, stats[x][y])
                temp = np.add(temp, stats[x][y])
            # print(temp)
            '''for z in range(len(stats[x][y])):  #
                    print(stats[x][y][z])'''
            # print(len(stats[x]))
            temp = temp/ len(stats[x])
            # print(avgs, temp.tolist())
            avgs.append(temp.tolist())
            # print(np.array(avgs))
        return avgs


def constraint_avg_runs(stats, morg):
    if morg is 'g':
        avgs = []  # len(stats[-1][0])] number of runs
        # print(avgs)
        # print(stats)
        temp = 0
        for x in range(len(stats)):  # run data
            temp = 0
            instances = 0
            for y in range(len(stats[x])):  # priorities data
                print(y, stats[x][y])
                if stats[x][y] != [0]:
                    instances += 1
                    temp = np.add(temp, stats[x][y])
            print('temp', temp)
            if type(temp) is not type(0):
                print(temp)
                print(instances)
                temp = temp/instances
                print(temp)
            else:
                temp = np.array([0])
            avgs.append(temp.tolist())
            # print('0', temp)
            '''
            for z in range(len(temp)):
                print('z', temp[z])
                # temp[z] = temp[z] / len(stats[x])
            # print(avgs, temp)
            avgs.append(temp.tolist())'''
            print(avgs)
        return avgs
    elif morg is 'm':
        # print('mcf')
        avgs = []
        # print(avgs)
        for x in range(len(stats)):  # run data
            # print('x')
            temp = stats[x][0]
            # print('0', temp)
            if temp is 0:
                avgs.append([0])
                continue
            for y in range(1, len(stats[x])):  #
                # print(y, stats[x][y])
                temp = np.add(temp, stats[x][y])
            # print(temp)
            '''for z in range(len(stats[x][y])):  #
                    print(stats[x][y][z])'''
            # print(len(stats[x]))
            print('mcf stats length', len(stats[x]))
            temp = temp/ len(stats[x])
            # print(avgs, temp.tolist())
            avgs.append(temp.tolist())
            # print(np.array(avgs))
        return avgs


def get_total_reroute_distance(stats, type):
    if type is 'g':
        totals = []  # len(stats[-1][0])] number of runs
        for x in range(len(stats)):
            temp = stats[x][0]
            # print('0', temp)
            if temp is 0:
                totals.append([0,0,0,0])
                continue
            else:
                tempz = [0,0,0,0]
                for z in range(len(stats[x])):
                    tempz[z] = np.sum(stats[x][z])
            # print(tempz)
            totals.append(tempz)
            # print(totals)
        return totals
    elif type is 'm':
        # print('mcf')
        totals = []
        for x in range(len(stats)):  # run data
            temp = stats[x][0]
            # print('0', temp)
            if temp is 0:
                totals.append(0)
                continue
            else:
                temp = np.sum(stats[x])
            totals.append(temp)
            # print(np.array(avgs))
        return totals

def cost_average(stats, type):
    if type is 'g':
        avgs = np.zeros([(len(stats)), len(stats[-1][0])])  # len(stats[-1][0])] number of runs
        # print(avgs)
        # print(stats)
        for x in range(len(stats)):  # run data
            # print(len(stats))
            temp = stats[x][0]
            print('0', temp)
            if temp is 0:
                continue
            else:
                tempz = [0,0,0,0]
                for z in range(len(stats[x][0])):
                    temp = np.sum(stats[x][0][z])
                    tempz[z] = temp
            for y in range(1, len(stats[x])):  # priorities data
                print(y, stats[x][y])
                # temp = np.add(temp, stats[x][y])
                for z in range(len(stats[x][y])):  #
                    print(stats[x][y][z])
                    temp = np.sum(stats[x][y][z])
                    print('sum of z', temp)
                    tempz[z] = tempz[z] + temp
                    print('tempz z', tempz[z])
            print(tempz)
            for z in range(len(tempz)):
                tempz[z] = tempz[z] / len(stats[x])
            print(avgs, tempz)
            avgs[x] = tempz
            '''for z in range(len(temp)):
                total = np.sum(temp[z])
                print(total)
                avgs[x][z] = total'''
            print(avgs)
        return avgs
    elif type is 'm':
        print('mcf')
        avgs = np.zeros([(len(stats))])
        # print(avgs)
        for x in range(len(stats)):  # run data
            print('x')
            temp = np.sum(stats[x][0])
            print('0', temp)
            for y in range(1, len(stats[x])):  #
                print(y, stats[x][y])
                temp = temp + np.sum(stats[x][y])
                print(temp)
                '''for z in range(len(stats[x][y])):  #
                    print(stats[x][y][z])'''
            print(len(stats[x]))
            total = temp / len(stats[x])
            print(avgs, total)
            avgs[x] = total
            # print(np.array(avgs))
        return avgs


def split_users_data(g, m, total, increment):
    j = increment
    k = total
    g1 = [[0]]
    # m1 = [[0]]
    m.insert(0, [0])
    while j <= k:
        print(j)
        # m1.append(m[j])
        temp = []
        for x in range(len(g)):
            print('g', g[x])
            temp.append(g[x][0:j])
            print(temp)
        g1.append(temp)
        j += increment
    return [g1, m]