from djikstra import dijkstra
from a_algorithm_time_criterion import a_algorithm_time_criterion
from a_algorithm_transfers_criterion import a_algorithm_transfers_criterion
from a_algorithm_hybrid import a_algorithm_hybrid
from a_algorithm_transfers_criterion_improved import a_algorithm_transfers_criterion_improved
import utils
import sys

def read_input():
    start_stop = input("Please enter the name of the starting stop\n")
    end_stop = input("Please enter the name of the end stop\n")
    start_time = input("Please enter the time (format hh:mm:ss)\n")
    mode = input("Please select: time criterion (t), transfers criterion (p)\n")
    return start_stop, end_stop, start_time, mode

def print_djikstr_solution(start_stop, end_stop, graph, start_time):
    print("\nDJIKSTRA SOLUTION\n")
    u, cost, benchmark_time = dijkstra(start_stop, end_stop, start_time, graph)
    print(u)
    print("Cost value: " + str(cost) + " seconds", file=sys.stderr)
    print("Time of execution: " + str(benchmark_time) + " seconds", file=sys.stderr)

def print_a_algorithm_time_criterion_solution(start_stop, end_stop, graph, start_time):
    print("\nA* ALGORITHM TIME CRITERION SOLUTION\n")
    path, cost, benchmark_time = a_algorithm_time_criterion(start_stop, end_stop, start_time, graph)
    print(path)
    print("Cost value: " + str(cost) + " seconds", file=sys.stderr)
    print("Time of execution: " + str(benchmark_time) + " seconds", file=sys.stderr)

def print_a_algorithm_transfers_criterion_solution(start_stop, end_stop, graph, start_time):
    print("\nA* ALGORITHM TRANSFERS CRITERION SOLUTION\n")
    path, cost, benchmark_time = a_algorithm_transfers_criterion(start_stop, end_stop, start_time, graph)
    print(path)
    print("Cost value: " + str(cost) + " transfers", file=sys.stderr)
    print("Time of execution: " + str(benchmark_time) + " seconds", file=sys.stderr)

def print_a_algorithm_transfers_criterion_solution_improved(start_stop, end_stop, graph, start_time):
    print("\nA* ALGORITHM TRANSFERS CRITERION SOLUTION IMPROVED COMPUTATIONAL TIME\n")
    path, cost, benchmark_time = a_algorithm_transfers_criterion_improved(start_stop, end_stop, start_time, graph)
    print(path)
    print("Cost value: " + str(cost), file=sys.stderr)
    print("Time of execution: " + str(benchmark_time) + " seconds", file=sys.stderr)

def main():
    start_stop, end_stop, start_time, mode = read_input()
    graph = utils.read_data("connection_graph.csv")
    if mode == 't':
        print_djikstr_solution(start_stop, end_stop, graph, start_time)
        print_a_algorithm_time_criterion_solution(start_stop, end_stop, graph, start_time)
    elif mode == 'p':
        print_a_algorithm_transfers_criterion_solution(start_stop, end_stop, graph, start_time)
        print_a_algorithm_transfers_criterion_solution_improved(start_stop, end_stop, graph, start_time)

if __name__ == '__main__':
    main()