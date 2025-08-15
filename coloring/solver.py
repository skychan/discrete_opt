#!/usr/bin/python
# -*- coding: utf-8 -*-
from ortools.sat.python import cp_model


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    # solution = range(0, node_count)
    solution = solve(node_count, edges)

    # prepare the solution in the specified output format
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def solve(nv, edges):
    model = cp_model.CpModel()
    color = [model.NewIntVar(0, nv, f'node {v}') for v in range(nv)]

    for edge in edges:
        v1, v2 = edge
        model.Add(color[v1] != color[v2])

    obj = model.NewIntVar(0, nv, 'obj')

    model.AddMaxEquality(obj, color)
    model.Minimize(obj)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 180
    solver.parameters.num_search_workers = 16
    solver.parameters.log_search_progress = True

    status = solver.Solve(model)

    return [solver.Value(v) for v in color]

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

