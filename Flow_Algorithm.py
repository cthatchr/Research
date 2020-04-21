from geopy import distance
from Station import *
from User import *
from StationDW import *
from DistList import *
from ortools.graph import pywrapgraph


def min_cost_alg(stations, users, constraint, individual=False, reroutes=False):
    split = split_stations(stations)
    surplus = split[0]
    deficit = split[1]
    mcf = pywrapgraph.SimpleMinCostFlow()
    if reroutes is False:
        reroutes = len(users)
    start_id = set_start_id(surplus, deficit)
    end_id = set_end_id(surplus, deficit)
    start_nodes = set_start_nodes(surplus, deficit)  # creates the start nodes
    end_nodes = set_end_nodes(surplus, deficit)  # creates end nodes
    capacities = set_capacities(start_nodes, end_nodes)  # creates the capacites for each arc
    costs = set_costs(start_nodes, end_nodes)  # creates the cost/distance for each node
    supplies = set_supplies(surplus, deficit, reroutes)  # assigns the supplies for each node
    source = 0
    sink = 999
    tasks = len(users)

    for i in range(0, len(start_nodes)):  # Add each Arc
        if (constraint is False) or (constraint > costs[i]):
            mcf.AddArcWithCapacityAndUnitCost(start_id[i], end_id[i], capacities[i], costs[i])

    mcf.SetNodeSupply(0, supplies[0])
    for i in range(1, len(supplies)-1):  # add supplies
        mcf.SetNodeSupply(i, supplies[i])
    mcf.SetNodeSupply(999, supplies[len(supplies)-1])

    if mcf.Solve() == mcf.OPTIMAL:
        if individual is True:
            mcf_costs = []
            for arc in range(mcf.NumArcs()):

                # Can ignore arcs leading out of source or into sink.
                if mcf.Tail(arc) != source and mcf.Head(arc) != sink:

                    # Arcs in the solution have a flow value of 1. Their start and end nodes
                    # give an assignment of worker to task.

                    if mcf.Flow(arc) > 0:
                        for x in range(mcf.Flow(arc)):
                            mcf_costs.append(mcf.UnitCost(arc))
                        '''print('%d user(s) from Station %d rerouted to station %d. Distance = %d' % (
                            mcf.Flow(arc),
                            mcf.Tail(arc),
                            mcf.Head(arc),
                            mcf.UnitCost(arc)))'''
            # print('Total distance = ', mcf.OptimalCost())
            # print()
            return mcf_costs
        else:
            # print('Total distance = ', mcf.OptimalCost())
            # print()
            return mcf.OptimalCost()
    else:
        print('There was an issue with the min cost flow input.')
        return 0




def split_stations(stations):  # splits stations into two lists, surplus and deficit
    surplus = []
    deficit = []
    for x in stations:
        if x.is_surplus():
            surplus.append(x)
        elif x.is_deficit():
            deficit.append(x)
    return [surplus, deficit]


def set_start_id(surplus, deficit):
    strt = [0] * len(surplus)
    for x in surplus:
        strt += [x.id] * len(deficit)
    for y in deficit:
        strt += [y.id]
    return strt


def set_end_id(surplus, deficit):  # creates the end nodes
    end = []
    for x in surplus:
        end += [x.id]
    for x in surplus:
        for y in deficit:
            end += [y.id]
    end += [999]*len(deficit)
    return end

def set_start_nodes(surplus, deficit):  # creates the start nodes
    strt = ['Source']*len(surplus)
    for x in surplus:
        strt += [x]*len(deficit)
    for y in deficit:
        strt += [y]
    return strt


def set_end_nodes(surplus, deficit):  # creates the end nodes
    end = []
    for x in surplus:
        end += [x]
    for x in surplus:
        for y in deficit:
            end += [y]
    end += ['Sink']*len(deficit)
    return end


def set_capacities(strt, end, reroutes = False):
    cap = []
    # if reroutes is False:
    for x in range(len(strt)):
        if strt[x] is 'Source':
            cap += [int(end[x].getdiff())]
        elif end[x] is 'Sink':
            cap += [int(strt[x].getdiff(absval=True))]
        else:
            cap += [int(strt[x].getdiff())]
    '''else:
        for x in range(len(strt)):
            if strt[x] is 'Source':
                cap += [int(reroutes)]
            elif end[x] is 'Sink':
                cap += [int(reroutes)]
            else:
                cap += [int(strt[x].getdiff())]'''
    return cap


def set_costs(strt, end):
    cost =[]
    for x in range(len(strt)):
        for x in range(len(strt)):
            if strt[x] is 'Source':
                cost += [0]
            elif end[x] is 'Sink':
                cost += [0]
            else:
                cost += [int(get_distance(strt[x], end[x]))]
        return cost


def set_supplies(surplus, deficit, amount):
    supplies = [amount]
    supplies += [0]*len(surplus)
    supplies += [0]*len(deficit)
    supplies += [-amount]
    return supplies


def print_flow(surplus, deficit):
    for x in surplus:
        print(x.id, x.getdiff(), end = '||')
    print()
    for x in deficit:
        print(x.id, x.getdiff(), end = '|')
    print()