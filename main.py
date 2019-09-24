from geopy import distance
from Algorithm import *
from Station import *
from User import *
from DistList import *
import numpy as np
import matplotlib.pyplot as plt
import citybikes
import pandas as pd
import json
from pandas.io.json import json_normalize
from datetime import datetime
import copy
import folium as fl
from Random import *
from Real import *
from Completion import *


def startup():
    choice = {}
    choice['1'] = "Random Data"
    choice['2'] = "Real Data"
    choice['3'] = "Completion"
    choice1 = {}
    choice1['1'] = "Greedy"
    choice1['2'] = "Min Cost Flow"
    choice1['3'] = "Compare Both"

    while True:
        options = choice.keys()
        for x in options:
            print(x, choice[x])

        selection = input("Select:")
        if selection == '1':
            set_rand_settings()
            break
        elif selection == '2':
            set_real_settings()
            break
        elif selection == '3':

            while True:
                options = choice1.keys()
                for x in options:
                    print(x, choice1[x])

                selection = input("Select:")
                if selection == '1':  # greedy
                    greedy_settings()
                    break
                elif selection == '2':  # mcf
                    mcf_settings()
                    break
                elif selection == '3':  # both

                    break
                else:
                    print('select again')
            break
        else:
            print('select again')


def test():
    s = Station()
    s1 = Station()
    s2 = Station()

    stations = [s, s1, s2]
    users = create_rand_users(stations,5)

    s.print_info()
    s1.print_info()
    s2.print_info()
    print(s.getdiff()+s1.getdiff()+s2.getdiff())
    delete_inc(stations)
    users = create_rand_users(stations, 5)

    s.print_info()
    s1.print_info()
    s2.print_info()
    print(s.getdiff() + s1.getdiff() + s2.getdiff())


startup()

