from a_algorithm_time_criterion import a_algorithm_time_criterion
from a_algorithm_transfers_criterion import a_algorithm_transfers_criterion_with_given_line
from time import time

from utils import SIMPLE_TABU_SEARCH_ITERATION_LIMIT

class Solution:
    def __init__(self, stops_in_order):
        self.stops_in_order = stops_in_order
        self.paths = []
        self.cost = -1
        self.estimated_cost = -1

    def set_paths(self, path_search_func, graph, start_time):
        curr_time = start_time
        self.cost = 0

        for i in range(len(self.stops_in_order) - 1):
            if path_search_func == a_algorithm_transfers_criterion_with_given_line:
                if i > 0:
                    path = path_search_func(self.stops_in_order[i], self.stops_in_order[i+1], curr_time, graph, self.paths[i-1][0].line_number)
                else:
                    path = path_search_func(self.stops_in_order[i], self.stops_in_order[i+1], curr_time, graph, -1)
            else:
                path = path_search_func(self.stops_in_order[i], self.stops_in_order[i+1], curr_time, graph)
            self.paths.append(path)
            if path_search_func == a_algorithm_transfers_criterion_with_given_line and i > 0:
                self.cost = self.cost + int(transfer_occured(self.paths[i-1][0], path[0]))
            curr_time = path[0].arrival_time
        
        for path in self.paths:
            self.cost = self.cost + path[1]

    def __repr__(self):
        result = ""
        reversed_paths = self.paths[::-1]
        for path in reversed_paths:
            result = result + repr(path[0])
            result = result + "\n"

        return result
    
def transfer_occured(prev_solution_node, solution_node):
    if prev_solution_node.line_number != solution_node.line_number:
        return True
    
    second_stop = solution_node

    while second_stop.previous_node.stop_name != prev_solution_node.stop_name:
        second_stop = second_stop.previous_node

    if prev_solution_node.previous_node.stop_name == second_stop.stop_name:
        return True
    
    return False
    
def get_a_algorithm(optimization_criterion):
    if optimization_criterion == 't':
        return a_algorithm_time_criterion
    elif optimization_criterion == 'p':
        return a_algorithm_transfers_criterion_with_given_line
    
def generate_solution(graph, stops_in_order, start_time, optimization_criterion):
    solution = Solution(stops_in_order)
    a_algorithm = get_a_algorithm(optimization_criterion)
    solution.set_paths(a_algorithm, graph, start_time)
    return solution

def get_starting_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    stops_in_order = [start_stop] + stops_to_visit + [start_stop]
    starting_solution = generate_solution(graph, stops_in_order, start_time, optimization_criterion)
    return starting_solution

def extract_first_node(end_node):
    node = end_node
    while node.previous_node != None:
        node = node.previous_node
    return node

def generate_estimated_solution(current_solution, stops_new_order, cost, i, graph, optimization_criterion):
    estimated_solution = Solution(stops_new_order)
    first_node = extract_first_node(current_solution.paths[i][0])
    curr_time = first_node.arrival_time
    a_algorithm = get_a_algorithm(optimization_criterion)
    if optimization_criterion == "t":
        second_node = a_algorithm(stops_new_order[i], stops_new_order[i+1], curr_time, graph)
        curr_time = second_node[0].arrival_time
        third_node = a_algorithm(stops_new_order[i], stops_new_order[i+2], curr_time, graph)
        curr_time = second_node[0].arrival_time
        forth_node = a_algorithm(stops_new_order[i], stops_new_order[i+3], curr_time, graph)
        alternative_cost = second_node[1] + third_node[1] + forth_node[1]
    else:
        first_line = first_node.line_number
        second_node = a_algorithm(stops_new_order[i], stops_new_order[i+1], curr_time, graph, first_line)
        second_line = second_node[0].line_number
        curr_time = second_node[0].arrival_time
        third_node = a_algorithm(stops_new_order[i], stops_new_order[i+2], curr_time, graph, second_line)
        third_line = third_node[0].line_number
        curr_time = second_node[0].arrival_time
        forth_node = a_algorithm(stops_new_order[i], stops_new_order[i+3], curr_time, graph, third_line)
        alternative_cost = second_node[1] + third_node[1] + forth_node[1]
    estimated_cost = current_solution.cost - cost + alternative_cost
    estimated_solution.estimated_cost = estimated_cost

    return estimated_solution

def generate_neighbourhood(current_solution, tabu, graph, optimization_criterion):
    neighbourhood = []
    neighbourhood_solutions = []

    for i in range(len(current_solution.stops_in_order) - 3):
        stops_new_order = current_solution.stops_in_order.copy()
        stops_new_order[i+1], stops_new_order[i+2] = stops_new_order[i+2], stops_new_order[i+1]
        if stops_new_order in tabu:
            continue
        cost = current_solution.paths[i][1] + current_solution.paths[i+1][1] + current_solution.paths[i+2][1]
        estimated_solution = generate_estimated_solution(current_solution, stops_new_order, cost, i, graph, optimization_criterion)
        neighbourhood_solutions.append(estimated_solution)
        neighbourhood.append(stops_new_order)

    return neighbourhood, neighbourhood_solutions

def tabu_search_modified(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    start_execution_time = time()
    current_solution = get_starting_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    tabu = [current_solution]
    best_solution = current_solution
    i = 0

    while i < SIMPLE_TABU_SEARCH_ITERATION_LIMIT:
        neighbourhood, neighbourhood_solutions = generate_neighbourhood(current_solution, tabu, graph, optimization_criterion)
        if len(neighbourhood) == 0:
            break

        current_solution = min(neighbourhood_solutions, key= lambda s: s.estimated_cost)
        current_solution = generate_solution(graph, current_solution.stops_in_order, start_time, optimization_criterion)

        if current_solution.cost < best_solution.cost:
            best_solution = current_solution

        tabu = tabu + neighbourhood
        i = i + 1

    return best_solution, time() - start_execution_time