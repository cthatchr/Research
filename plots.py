import matplotlib.pyplot as plt
from Completion import *
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
    df = load_df()

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

    df['variance'] = sd_dist(150, load_stations())
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name",
                            hover_data=["totalDocks", "docksAvailable"],
                            color="variance", color_continuous_scale=px.colors.cyclical.IceFire,
                            size='totalDocks', zoom=10)

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=12, mapbox_center={"lat": 39.953555, "lon": -75.164042})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
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
    plt.ylabel('Distance(Meters)')
    # plt.plot(index, dist[0], label='Diff/Dist')
    plt.plot(index, dist[0], label='Diff/Dist^2')
    plt.plot(index, dist[1], label='Diff^2/Dist')
    plt.plot(index, dist[2], label='Only Dist')
    # plt.plot(index, dist[4], label='Only Diff')
    plt.plot(index, dist[3], label='Random')
    if mcf is not None:
        plt.axhline(y=mcf, xmin=0.90)
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    if name:
        name = 'U'+str(name[0])+'R'+str(name[1])+str(name[2])+'Const'+str(name[3][1])+'.png'
        plt.savefig(name)
    plt.show()

def compare_users_bar(index, greedy, greedy_const, mcf, mcf_const):
    x = np.arange(index)
    width = 0.25  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, greedy, width, label='greedy nc')
    rects2 = ax.bar(x - width / 4, greedy_const, width, label='greedy c')
    rects3 = ax.bar(x - width / 2, mcf, label='mcf nc')
    rects4 = ax.bar(x + width / 2, mcf_const, width, label='mcf c')
    ax.set_ylabel('Distance(meters)')
    ax.set_title('Users Rerouted per test')
    plt.show()
