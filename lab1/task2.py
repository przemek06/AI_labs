import utils
import sys
from tabu_search_modified import tabu_search_modified
from tabu_search import tabu_search
from T_tabu_search import T_tabu_search
from tabu_search_aspiration import tabu_search_aspiration

def read_input():
    start_stop = input("Please enter the name of the starting stop\n")
    stops_to_visit = input("Please enter the names of stops to visit\n")
    start_time = input("Please enter the time (format hh:mm:ss)\n")
    optimization_criterion = input("Please select: time criterion (t), transfers criterion (p)\n")
    return start_stop, stops_to_visit, start_time, optimization_criterion

def print_tabu_search_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    solution, execution_time = tabu_search(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("Tabu without T")
    print(solution)
    print("Cost: " + str(solution.cost))
    print("Time of execution: " + str(execution_time) + " seconds", file=sys.stderr)

def print_tabu_search_modified_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    solution, execution_time = tabu_search_modified(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("Tabu with sampling")
    print(solution)
    print("Cost: " + str(solution.cost))
    print("Time of execution: " + str(execution_time) + " seconds", file=sys.stderr)

def print_T_tabu_search_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    solution, execution_time = T_tabu_search(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("Tabu with T")
    print(solution)
    print("Cost: " + str(solution.cost))
    print("Time of execution: " + str(execution_time) + " seconds", file=sys.stderr)

def print_tabu_search_aspiration_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion):
    solution, execution_time = tabu_search_aspiration(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("Tabu with aspiration")
    print(solution)
    print("Cost: " + str(solution.cost))
    print("Time of execution: " + str(execution_time) + " seconds", file=sys.stderr)

def main():
    start_stop, stops_to_visit_str, start_time, optimization_criterion = read_input()
    graph = utils.read_data("connection_graph.csv")
    stops_to_visit = stops_to_visit_str.split(',')

    print_tabu_search_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("\n")
    print_T_tabu_search_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("\n")
    print_tabu_search_aspiration_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("\n")
    print_tabu_search_modified_solution(graph, start_stop, stops_to_visit, start_time, optimization_criterion)
    print("\n")


if __name__ == '__main__':
    main()