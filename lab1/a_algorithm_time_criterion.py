import numpy as np
import utils
from time import time
import geopy.distance

class Node:
    def __init__(self, stop_name, longitude, latitude, previous_node):
        self.stop_name = stop_name
        self.f = 0
        self.g = 0
        self.h = 0
        self.longitude = longitude
        self.latitude = latitude
        self.previous_node = previous_node
        self.line_number = None
        self.prev_departure_time = None
        self.arrival_time = None

    def __repr__(self):
        next = repr(self.previous_node) if self.previous_node is not None else " "
        return self.stop_name + ", arrived at " + str(self.arrival_time) + " on line " + str(self.line_number) + ", departed from the previous stop at " + str(self.prev_departure_time) + "\n" + next


def get_start_node(stop_a, graph, start_time):
    departures = utils.get_all_stops_with_departure_stop(stop_a, graph)
    longitude = departures[0][7]
    latitude = departures[0][8]
    start_node = Node(stop_a, longitude, latitude, None)
    start_node.arrival_time = start_time
    start_node.prev_departure_time = "--:--:--"
    start_node.line_number = "-"
    return start_node

def get_end_node(stop_b, graph):
    departures = utils.get_all_stops_with_departure_stop(stop_b, graph)
    longitude = departures[0][7]
    latitude = departures[0][8]
    return Node(stop_b, longitude, latitude, None)

def get_fastest_departure_for_node(departures, name, curr_time):
    filter_arr = np.asarray([name])
    mask = np.in1d(departures[:, 6], filter_arr)
    fastest_departure = min(departures[mask], key = lambda row: calc_overall_time(row, curr_time))
    return fastest_departure

def get_neighbourhood(node, graph, curr_time):
    departures = utils.get_all_stops_with_departure_stop(node.stop_name, graph)
    neighbour_names = np.unique(departures[:, 6])
    return [get_fastest_departure_for_node(departures, neighbour_name, curr_time) for neighbour_name in neighbour_names]

def h_eval(node, end):
    coords_1 = (float(node.longitude), float(node.latitude))
    coords_2 = (float(end.longitude), float(end.latitude))

    return (geopy.distance.geodesic(coords_1, coords_2).km ** 2) * utils.SPEED_COST_PARAMETER

def f_eval(node):
    return node.h + node.g

def calc_overall_time(row, curr_time):
        waiting_time = utils.time_difference(curr_time, utils.time_to_number(row[3]))
        drive_time = utils.time_difference(utils.time_to_number(row[3]), utils.time_to_number(row[4]))
        overall_time = waiting_time + drive_time
        return overall_time

def construct_next_node(prev_node, next_departure, time_diff, end_node):
    next_node = Node(str(next_departure[6]), next_departure[9], next_departure[10], prev_node)
    next_node.g = prev_node.g + time_diff
    next_node.h = h_eval(next_node, end_node)
    next_node.f = f_eval(next_node)
    next_node.prev_departure_time = next_departure[3]
    next_node.arrival_time = next_departure[4]
    next_node.line_number = next_departure[2]
    return next_node

def a_algorithm_time_criterion(stop_a, stop_b, start_time, graph):
    benchmark_time = time()
    start = get_start_node(stop_a, graph, start_time)
    end = get_end_node(stop_b, graph)
    open = {start.stop_name: start}
    closed = {}

    while len(open) > 0:
        min_node = min(open.values(), key=lambda node: node.f)
        curr_time = utils.time_to_number(start_time) + min_node.g

        if curr_time > utils.SECONDS_IN_DAY:
            curr_time = curr_time - utils.SECONDS_IN_DAY

        if min_node.stop_name == stop_b:
            return min_node, min_node.g, time() - benchmark_time
        
        open.pop(min_node.stop_name)
        closed[min_node.stop_name] = min_node

        neigbour_departures = get_neighbourhood(min_node, graph, curr_time)

        for next_departure in neigbour_departures:
            time_diff = calc_overall_time(next_departure, curr_time)
            if next_departure[6] not in closed and next_departure[6] not in open:
                next_node = construct_next_node(min_node, next_departure, time_diff, end)
                open[next_node.stop_name] = next_node
            elif next_departure[6] in open:
                next_node = open[next_departure[6]]
                if next_node.g > min_node.g + time_diff:
                    next_node = construct_next_node(min_node, next_departure, time_diff, end)
                    open[next_node.stop_name] = next_node
            elif next_departure[6] in closed:
                next_node = closed[next_departure[6]]
                if next_node.g > min_node.g + time_diff:
                    next_node = construct_next_node(min_node, next_departure, time_diff, end)
                    open[next_node.stop_name] = next_node
                    closed.pop(next_node.stop_name)



