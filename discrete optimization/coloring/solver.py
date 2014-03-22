#!/usr/bin/python
# -*- coding: utf-8 -*-


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
#    solution = range(0, node_count)

    # get all the nodes' neighbors:
    neighbors = []
    for i in xrange(node_count):
    	temp = set([i])
    	for k in edges:
    		if i in k:
    			temp|= set(k)
    	neighbors.append(temp)


    # dirty coloring
    solution = [None]*node_count
    nodes = [x for x in xrange(node_count)]
    nodes.sort(key = lambda i: len(neighbors[i]),reverse = True)
    
    #k = 0
    solution[nodes[0]] = 0
    for i in nodes[1:]:
        node = neighbors[i]
        colors = [0]
        node = list(node)
        node.sort()
        if solution[i] == None:
            for col in node:
                colors.append(solution[col])
            colors = list(set(colors)-set([None]))
            m = max(colors) +2
            t = list(set(xrange(m))-set(colors))
            solution[i] = min(t)
    '''
            
        for color in node:
            colors.append(solution[color])
        m = max(colors) + 2
        if solution[k] in colors:
            t = list(set(xrange(m))-set(colors))
            t.sort()
            solution[k] = t[0]            
        #k += 1
    '''

    s = min(solution)
    if s:
        solution = [solution[x]-s for x in xrange(node_count)]
    
    solution = [i for i in xrange(node_count)]
    # class the colors
    Class = [None]*(max(solution)+1)
    t = 0
    for node in solution:
        if Class[node] == None:
            Class[node] = [t]
        else:
            Class[node].append(t)
        t += 1
    Class.sort(key = len)

    # let's swap
    def bar(x):
        xn = set()
        for i in x:
            xn |= set(neighbors[i])
        return xn - set(x)
    
    while True:
        modify = 0
        for i in xrange(len(Class)):
                for j in xrange(i+1,len(Class)):
                    a = Class[i]
                    b = Class[j]
                    if a and b:
                        an = bar(a)
                        bn = bar(b)
                        aset = bn & set(a)
                        bset = an & set(b)
                        if aset:
                            at = (set(a)-aset)|bset
                            bt = (set(b)-bset)|aset
                            if len(bt)**2 + len(at)**2 > len(a)**2 + len(b)**2:
                                Class[i] = list(at)
                                Class[j] = list(bt)
                                modify = 1
                        else:
                            bt = list(set(b)|set(a))
                            Class[j] = bt
                            Class[i] = []
                            modify = 2
        while Class.count([]):
            Class.remove([])
            Class.sort(key= len)
        if modify == 0:
            break




    '''
                a = ta[-1]
                an = bar(a)
                b = ta[i]
                if b:
                    bset = an & set(b)
                    if bset :
                        bn = bar(b)
                        aset = bn & set(a)
                        if len(aset) < len(bset):
                            at = list((set(a)|bset) -aset)
                            bt = list((set(b)|aset) -bset)
                            ta[-1] = at
                            ta[i] = bt
                            modify = 1                   
                    else:
                        at = list(set(a)|set(b))
                        ta[-1] = at
                        ta[i] = []
                        modify = 2
            while ta.count([]):
                ta.remove([])
            tt.append(a)
            ta.pop()
        tt.sort(key = len)
        print tt
        Class = tt
#        Class.sort(key = len, reverse = True)
        if modify == 0:
            break'''
   
    
    node_count = len(Class)
    # coloring
    color = 0
    for nodes in Class:
        for node in nodes:
            solution[node] = color

        color += 1


    # check 
    
    c = []
    for i in edges:
        temp = solution[i[0]] - solution[i[1]]
        c.append(temp)
    if 0 in c:
        a = 0
    else:
        a = 1



    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(a) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

