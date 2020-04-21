import matplotlib.pyplot as plt
from Completion import *
from Station import *
from gmplot import gmplot
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



def station_map_gmp(stations):
    # Place map
    gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)

    # Polygon
    golden_gate_park_lats, golden_gate_park_lons = zip(*[
        (37.771269, -122.511015),
        (37.773495, -122.464830),
        (37.774797, -122.454538),
        (37.771988, -122.454018),
        (37.773646, -122.440979),
        (37.772742, -122.440797),
        (37.771096, -122.453889),
        (37.768669, -122.453518),
        (37.766227, -122.460213),
        (37.764028, -122.510347),
        (37.771269, -122.511015)
    ])
    gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)

    # Scatter points
    top_attraction_lats, top_attraction_lons = zip(*[
        (37.769901, -122.498331),
        (37.768645, -122.475328),
        (37.771478, -122.468677),
        (37.769867, -122.466102),
        (37.767187, -122.467496),
        (37.770104, -122.470436)
    ])
    gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

    # Draw
    gmap.draw("my_map.html")


def station_map():
    df = load_plot_stations()

    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", hover_data=["totalDocks", "docksAvailable"],
                              color_discrete_sequence=['red'], zoom=3, height=1000)

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=12, mapbox_center={"lat": 39.953555, "lon": -75.164042})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
    '''color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)'''


def station_map_scale():
    df = load_df()
    df['variance'] = sd_dist(250, load_stations())
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name",
                            hover_data=["totalDocks", "docksAvailable"],
                            color="variance", color_continuous_scale=px.colors.cyclical.IceFire,
                            size='totalDocks', zoom=10)

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=12, mapbox_center={"lat": 39.953555, "lon": -75.164042})
    fig.update_layout(width= 1500, height=1000, margin={"r": 0, "t": 15, "l": 0, "b":0})
    fig.show()
    '''color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)'''


def test_distribution(v):
    bins = np.arange(min(v), max(v) + 2) - 0.5
    plt.hist(v, bins)
    plt.xticks(range(min(v), max(v) + 1))
    plt.xlim([min(v) - 1, max(v) + 1])
    print(min(v), max(v))
    print(np.arange(min(v), max(v) + 1))
    plt.show()


def compare_dist(index, dist, dist_const, mcf=None, mcf_const=None, name=None):
    # create a line plot given a set of data
    plt.figure()
    plt.subplots_adjust(hspace=1)
    # plot non constraint
    plt.subplot(211)
    plt.title('No constraint')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(meters)')
    # plt.plot(index, dist[0], label='Diff/Dist')
    plt.plot(index, dist[0], label='Diff/Dist^2')
    plt.plot(index, dist[1], label='Diff^2/Dist')
    plt.plot(index, dist[2], label='Only Dist')
    # plt.plot(index, dist[4], label='Only Diff')
    plt.plot(index, dist[3], label='Random')
    if mcf is not None:
        plt.axhline(y=mcf_const, xmin=0.90, ls='dashed')

    plt.locator_params(axis='y', nbins=5)
    # plot constraint
    plt.subplot(212)
    plt.title('Constraint')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(meters)')
    # plt.plot(index, dist_const[0], label='Diff/Dist')
    plt.plot(index, dist_const[0], label='Diff/Dist^2')
    plt.plot(index, dist_const[1], label='Diff^2/Dist')
    plt.plot(index, dist_const[2], label='Only Dist')
    # plt.plot(index, dist_const[4], label='Only Diff')
    plt.plot(index, dist_const[3], label='Random')
    if mcf_const is not None:
        plt.axhline(y=mcf, xmin=0.90, ls='dashed')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    if name:
        name = 'Both'+'U'+str(name[0])+'R'+str(name[1])+str(name[2])+'Const'+str(name[3][1])+'.png'
        plt.savefig(name)
    plt.show()


def create_dist_plot(index, dist, mcf=None, name=None):
    # user distance moved
    plt.figure()
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Kilometers)')
    # plt.plot(index, dist[0], label='Diff/Dist')
    plt.plot(index, dist[0], label='Diff/Dist^2', marker='o')
    plt.plot(index, dist[1], label='Diff^2/Dist', marker='o')
    plt.plot(index, dist[2], label='Only Dist', marker='o')
    # plt.plot(index, dist[4], label='Only Diff')
    plt.plot(index, dist[3], label='Random', marker='o')
    if mcf is not None:
        plt.axhline(y=mcf, color='m', ls='dashed')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    if name:
        name = 'U'+str(name[0])+'R'+str(name[1])+str(name[2])+'Const'+str(name[3][1])+'.png'
        plt.savefig(name)
    # plt.show()


def compare_users_plot(index, greedy, mcf, cost, name=None):
    plt.figure()
    if cost is False:
        plt.title('Total Distance Rerouted vs. Total Users Rerouted')
        plt.xlabel('Total Users Rerouted')
        plt.ylabel('Distance(Kilometers)')
    else:
        plt.title('Cost vs. Total Users Rerouted')
        plt.xlabel('Total Users Rerouted')
        plt.ylabel('Cost')
    for x in index:
        print(x)
    plt.plot(index, (np.array(greedy[:,0], dtype='f')/1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[:,1], dtype='f')/1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[:,2], dtype='f')/1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[:,3], dtype='f')/1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f')/1000), label='MCF', marker='*')
    plt.legend()
    '''if name:
        name = 'UserIter'+'U'+str(name[0])+'R'+str(name[1])+str(name[2])+'Const'+str(name[3][1])+'.png'
        plt.savefig(name)'''
    plt.show()


def user_cost_plot(index, greedy_a, mcf_a):
    greedy = np.array(greedy_a[0])
    greedy_power = np.array(greedy_a[1])
    greedy_step = np.array(greedy_a[2])
    mcf = np.array(mcf_a[0])
    mcf_power = np.array(mcf_a[1])
    mcf_step = np.array(mcf_a[2])

    # Distance
    plt.figure(1)
    plt.title('Cost vs. Users Rerouted')
    plt.ylabel('Distance')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_Dist')

    # Distance^2
    plt.figure(2)
    plt.title('Cost vs. Users Rerouted')
    plt.ylabel('$Distance^2$')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy_power[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_power[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_power[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_power[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_power, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_Squared')


    # Step
    plt.figure(3)
    plt.title('Cost vs. Users Rerouted')
    plt.ylabel('Step Function')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy_step[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_step[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_step[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_step[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_step, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_Step')
    plt.show()


def user_average_reroute(index, greedy_a, mcf_a):
    greedy = np.array(greedy_a[0])
    greedy_power = np.array(greedy_a[1])
    greedy_step = np.array(greedy_a[2])
    mcf = np.array(mcf_a[0])
    mcf_power = np.array(mcf_a[1])
    mcf_step = np.array(mcf_a[2])

    # Distance
    plt.figure(1)
    plt.title('Average Cost vs. Users Rerouted')
    plt.ylabel('Distance')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_AvgDist')

    # Distance^2
    plt.figure(2)
    plt.title('Average Cost vs. Users Rerouted')
    plt.ylabel('$Distance^2$')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy_power[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_power[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_power[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_power[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_power, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_AvgSquared')


    # Step
    plt.figure(3)
    plt.title('Average Cost vs. Users Rerouted')
    plt.ylabel('Step Function')
    plt.xlabel('Users Rerouted')
    plt.plot(index, (np.array(greedy_step[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_step[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_step[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_step[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_step, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    plt.savefig('U_AvgStep')
    plt.show()


def constraint_avg_reroute(index, greedy_a, mcf_a):
    greedy = np.array(greedy_a[0])
    greedy_power = np.array(greedy_a[1])
    greedy_step = np.array(greedy_a[2])
    mcf = np.array(mcf_a[0])
    mcf_power = np.array(mcf_a[1])
    mcf_step = np.array(mcf_a[2])

    plt.figure(1)
    plt.title('Average Cost vs. Constraint')
    plt.ylabel('Distance')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f') / 1000), label='MCF', marker='*')
    plt.ylim(ymin=0)
    plt.savefig('C_AvgDist')
    plt.legend()

    # Distance^2
    plt.figure(2)
    plt.title('Average Cost vs. Constraint')
    plt.ylabel('$Distance^2$')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy_power[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_power[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_power[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_power[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_power, dtype='f') / 1000), label='MCF', marker='*')
    plt.ylim(ymin=0)
    plt.savefig('C_AvgSquared')
    plt.legend()

    # Step
    plt.figure(3)
    plt.title('Average Cost vs. Constraint')
    plt.ylabel('Step Function')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy_step[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_step[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_step[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_step[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_step, dtype='f') / 1000), label='MCF', marker='*')
    plt.ylim(ymin=0)
    plt.savefig('C_AvgStep')
    plt.legend()
    plt.show()


def constraint_cost_plot(index, greedy_a, mcf_a):
    greedy = np.array(greedy_a[0])
    greedy_power = np.array(greedy_a[1])
    greedy_step = np.array(greedy_a[2])
    mcf = np.array(mcf_a[0])
    mcf_power = np.array(mcf_a[1])
    mcf_step = np.array(mcf_a[2])
    # print(greedy)
    # print(greedy_power)
    # print(greedy_step)
    # print(mcf)
    # print(mcf_power)
    # print(mcf_step)

    # Distance
    plt.figure(1)
    plt.title('Cost vs. Reroute Constraint')
    plt.ylabel('Distance')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f') / 1000), label='MCF', marker='*')
    plt.ylim(ymin=0)
    plt.savefig('C_Dist')
    plt.legend(fontsize=18, prop={'size': 13})

    # Distance^2
    plt.figure(2)
    plt.title('Cost vs. Reroute Constraint')
    plt.ylabel('$Distance^2$')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy_power[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_power[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_power[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_power[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_power, dtype='f') / 1000), label='MCF', marker='*')
    plt.ylim(ymin=0)
    plt.savefig('C_Squared')
    plt.legend(prop={'size': 12})

    # Step
    plt.figure(3)
    plt.title('Cost vs. Reroute Constraint')
    plt.ylabel('Step Function')
    plt.xlabel('Constraint')
    plt.plot(index, (np.array(greedy_step[:, 0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy_step[:, 1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy_step[:, 2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy_step[:, 3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf_step, dtype='f') / 1000), label='MCF', marker='*')
    plt.savefig('C_Step')
    plt.ylim(ymin=0)
    plt.legend(prop={'size': 12})
    plt.show()


def compare_constraint_plot(index, greedy, mcf, name=None):
    plt.figure()
    plt.title('Total Distance Rerouted vs. Constraint')
    plt.xlabel('Constraint')
    plt.ylabel('Distance(Kilometers)')
    plt.plot(index, (np.array(greedy[0], dtype='f') / 1000), label='Diff/Dist^2', marker='^')
    plt.plot(index, (np.array(greedy[1], dtype='f') / 1000), label='Diff^2/Dist', marker='o')
    plt.plot(index, (np.array(greedy[2], dtype='f') / 1000), label='Only Dist', marker='s')
    plt.plot(index, (np.array(greedy[3], dtype='f') / 1000), label='Random', marker='d')
    plt.plot(index, (np.array(mcf, dtype='f') / 1000), label='MCF', marker='*')
    plt.legend()
    if name:
        name = 'ConstraintIter'+'U'+str(name[0])+'R'+str(name[1])+str(name[2])+'Const'+str(name[3][1])+'.png'
        plt.savefig(name)
    plt.show()


def fail_rate(index, failures):
    plt.figure(1, figsize=(10,5))
    plt.title('Failure Rate vs. Constraint')
    plt.ylabel('Failure Rate')
    plt.xlabel('Constraint')
    x_pos = np.arange(len(index))
    # width = .40
    # x_pos = [x + width for x in x_pos]

    plt.bar(x_pos, failures)
    plt.xticks(x_pos, index)
    plt.savefig('Failure Rate')
    # plt.legend()
    plt.show()

def fail_rate_stacked(index, failures):
    plt.figure(1, figsize=(10, 5))
    plt.title('Failure Rate vs. Constraint')
    plt.ylabel('Failure Rate')
    plt.xlabel('Constraint')
    x_pos = np.arange(len(index))
    p1 = failures[0]
    p2 = failures[1]
    p3 = failures[2]
    h3 = np.add(p1, p2).tolist()
    print(p1)
    print(p2)
    print(h3)
    p4 = failures[3]
    h4 = np.add(h3, p3).tolist()
    print(h4)
    width = .40
    # x_pos = [x + width for x in x_pos]

    plt.bar(x_pos, p1, label='Diff/Dist^2')
    plt.bar(x_pos, p2, bottom=p1, label='Diff^2/Dist')
    plt.bar(x_pos, p3, bottom=h3, label='Only Dist')
    plt.bar(x_pos, p4, bottom=h4,  label='Random')
    plt.xticks(x_pos, index)
    plt.savefig('Failure Rate')
    plt.legend()
    plt.show()


def priority_fails(failures, instances):
    data = []
    priorities = len(failures[0])
    for y in range(priorities):
        temp = [item[y] for item in failures]
        print(y, temp)
        for x in range(len(temp)):
            try:
                temp[x] = temp[x]/instances
                temp[x] = temp[x] / priorities
            except ZeroDivisionError:
                temp[x] = 0
        data.append(temp)
    return data



def fail_rate_all(index, failures):
    fig, ax = plt.subplots(figsize=(15,5))
    width = .40
    ax.set_title('Failure Rate vs. Constraint')
    ax.set_ylabel('Failure Rate')
    ax.set_xlabel('Constraint')
    x = np.arange(0, (2* len(index)), 2)
    x1 = [x + width for x in x]
    x2 = [x + width for x in x1]
    # x3 = [x + width for x in x2]

    print(x)
    print(x1)
    print(x2)
    # print(x3)


    ax.bar(x, failures[0], width=width, label = 'Normal', align='center', edgecolor='white')  # normal
    ax.bar(x1, failures[1], width=width, label = 'Uniform', align='center', edgecolor='white')  # uniform
    ax.bar(x2, failures[2], width=width, label = 'Exponent', align='center', edgecolor='white')  # exponential
    # ax.bar(x3, failures[3], width=width, label = 'Random', align='center', edgecolor='white')  # random

    ax.set_xticklabels(index)
    ax.set_xticks(x+width)
    # plt.autoscale()
    ax.legend(prop={'size': 6})
    plt.savefig('Failure Rate')
    plt.show()