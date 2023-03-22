import numpy as np
import utils
from time import time

class Node:
    def __init__(self, stop_name, cost, previous_node):
        self.stop_name = stop_name
        self.cost = cost
        self.previous_node = previous_node
        self.arrival_time = None
        self.prev_departure_time = None
        self.line_number = None

    def __repr__(self) -> str:
        next = repr(self.previous_node) if self.previous_node is not None else " "
        return self.stop_name + ", arrived at " + str(self.arrival_time) + " on line " + str(self.line_number) + ", departed from the previous stop at " + str(self.prev_departure_time) + "\n" + next

def create_node(name):
    return Node(name, float("inf"), None)

def get_all_nodes(graph):
    return {node_name: create_node(node_name) for node_name in np.unique(graph[:, 5])}

def init_first_node(u, start_time):
    u.cost = 0
    u.arrival_time = start_time
    u.line_number = "-"
    u.prev_departure_time = "--:--:--"

def dijkstra(stop_a, stop_b, start_time, graph):
    algorithm_start_time = time()
    Q = get_all_nodes(graph)
    u = Q[stop_a]
    init_first_node(u, start_time)
    start_time = utils.time_to_number(start_time)

    while len(Q) > 0:
        u = min(Q.values(), key=lambda node: node.cost)
        curr_time = start_time + u.cost

        if curr_time > utils.SECONDS_IN_DAY:
            curr_time = curr_time - utils.SECONDS_IN_DAY

        if u.stop_name == stop_b:
            return u, u.cost, time() - algorithm_start_time

        Q.pop(u.stop_name, None)
        departures = utils.get_all_stops_with_departure_stop(u.stop_name, graph)

        for departure in departures:
            arrival_stop_name = departure[6]
            if arrival_stop_name not in Q.keys():
                continue

            arrival_node = Q[arrival_stop_name]
            waiting_time = utils.time_difference(curr_time, utils.time_to_number(departure[3]))
            drive_time = utils.time_difference(utils.time_to_number(departure[3]), utils.time_to_number(departure[4]))
            calculated_cost = u.cost + waiting_time + drive_time

            if calculated_cost < arrival_node.cost:
                arrival_node.cost = calculated_cost
                arrival_node.previous_node = u
                arrival_node.arrival_time = departure[4]
                arrival_node.prev_departure_time = departure[3]
                arrival_node.line_number = departure[2]