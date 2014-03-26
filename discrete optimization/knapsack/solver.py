#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in xrange(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
    table = [[0]*(capacity+1)]
#    table = [[]]

    # begin to table the value
    for i in xrange(item_count):
        item = items[i]
        s = []
        for k in xrange(0, capacity+1):  
            if i == 0:
                if item.weight <= k:
                    s.append(item.value)
                else:
                    s.append(0)                    
            elif item.weight <= k:
                temp = max(table[i][k], item.value + table[i][k-item.weight])
                s.append(temp)
            else:
                temp = table[i][k]
                s.append(temp)
        table.append(s)

    value = table[item_count][capacity]
    # begin to pick the var
    for j in xrange(item_count-1,0,-1):
        item = items[j]        
        if table[j+1][capacity] == table[j][capacity] :
            taken[j] = 0
        else:
            taken[j] = 1
            capacity = capacity - item.weight
            if capacity == 0:
                break
    
#        taken[item.index] = 1
#        value += item.value
#       weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

