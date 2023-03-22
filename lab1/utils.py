from pandas import read_csv
import numpy as np

SECONDS_IN_DAY = 60*60*24
SPEED_COST_PARAMETER = 3600/15
TRANSFER_SPEED_COST_PARAMETER = 1/8
HYBRID_COST_PARAMETER = 8
HYBRID_TIME_COST_CONVERSION_RATIO = 1/600
SIMPLE_TABU_SEARCH_ITERATION_LIMIT = 50
LOCAL_TABU_LIMIT = 10

def read_data(file_name):
    df = read_csv(file_name, index_col = 0, dtype='unicode')
    return df.to_numpy()

def time_to_number(time_str):
    time_parts = time_str.split(":")
    time_int = 60*60*int(time_parts[0]) + 60*int(time_parts[1]) + int(time_parts[2])
    return time_int

def number_to_time(time):
    seconds = time % 60
    time = time // 60
    minutes = time % 60
    time = time // 60
    hours = time % 24
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

def time_difference(time_int_1, time_int_2):
    if time_int_2 >= time_int_1:
        return time_int_2 - time_int_1
    else:
        return SECONDS_IN_DAY - (time_int_1 - time_int_2)

def get_all_stops_with_departure_stop(departure_stop, graph):
    filter_arr = np.asarray([departure_stop])
    mask = np.in1d(graph[:, 5], filter_arr)
    return graph[mask]

def get_only_correct_way(departures, prev_node):
    excldued_stop_name = prev_node.previous_node.stop_name if prev_node.previous_node is not None else None
    filter_arr = np.asarray([excldued_stop_name])
    mask = np.in1d(departures[:, 6], filter_arr)
    return departures[np.invert(mask)]