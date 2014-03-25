#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randrange

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
	print 'edges done'

	# build a trivial solution
	# every node has its own color


	# get all the nodes' neighbors:
	neighbors = []
	for i in xrange(node_count):
		temp = set([i])
		for k in edges:
			if i in k:
				temp|= set(k)
		neighbors.append(temp)
	print 'neighbors done'


	# dirty coloring and sort by node's degree
	#solution = [0]*node_count
	nodes = [x for x in xrange(node_count)]
	#nodes.sort(key = lambda i: len(neighbors[i]),reverse = True)
	#print 'init.....'
	
	def generateclass(solution):
		c = [[]]*(max(solution)+1)
		t = 0
		for node in solution:
			if c[node] == []:
				c[node] = [t]
			else:
				c[node].append(t)
			t += 1
		return c

	def f(Class):
		Bad = Bad_edge(Class)
		n = len(Bad)
		v = 0
		for i in xrange(n):
			b = len(Bad[i])
			c = len(Class[i])
			v += 2*b*c - c**2
		return n,v

	def ff(Class):
		n = len(Class)
		v = 0
		for i in xrange(n):
			c = len(Class[i])
			v += c**2
		return v

	def bar(x):
		xn = set()
		for i in x:
			xn |= set(neighbors[i])
		return xn - set(x)

	def foo(x,y):
		xn = bar(x)
		yn = bar(y)
		xset = yn & set(x)
		yset = xn & set(y)
		return xset,yset

	def updatesolution(at,bt,i,j,tempsolution):
		for node in at:
			tempsolution[node] = i
		for node in bt:
			tempsolution[node] = j
		return tempsolution

	def update(Class):
		while Class.count([]):
			Class.remove([])
		solution = [0]*node_count
		for color in xrange(len(Class)):
			for node in Class[color]:
				solution[node] = color
		return solution

	def sswap(a,b):
		if a and b:
			aset,bset = foo(a,b)
			if aset:
				at = (set(a)-aset)|bset
				bt = (set(b)-bset)|aset
			else:
				at = set(a)|set(b)
				bt = set()
		att = list(at)
		btt = list(bt)
		att.sort()
		btt.sort()
		return att,btt

	def delta(a,b,at,bt):
		deltas = 0
		l1 = len(a)
		l2 = len(b)
		l3 = len(at)
		l4 = len(bt)
		deltas = l3**2 + l4**2 -l1**2 -l2**2
		return deltas

	def neighborcolor(node):
		color = []
		domain = list(set(neighbors[node]))
		for neighbor in domain:
			color.append(solution[neighbor])
		ncolor = set(color)
		return len(ncolor),ncolor

	def gam(ocolor,newcolor,Class):
		l1 = Class[ocolor]
		l2 = Class[newcolor]
		return 2-2*len(l1)+2*len(l2)

	#solution = [x for x in xrange(node_count)]
	#global Class
	solution = [0]*node_count
	k = 0
	for node in neighbors:
		colors = []
		for color in node:
			colors.append(solution[color])
			m = max(colors) + 2
		if solution[k] in colors:
			t = list(set(xrange(m))-set(colors))
			t.sort()
			solution[k] = t[0]
		k += 1
	mins = min(solution)
	if mins:
		solution = [solution[x]-mins for x in xrange(node_count)]
	
	#node_count = set(solution)
	Class = generateclass(solution)

	print 'greedy done'

	star = solution[:]
	s = ff(Class)
	tabu = [[]]*200
	#tabu.append(star[:])
	aspiration = [[]]*30
	colorn = len(Class)
	M = 5000
	L = 0
	AAA = xrange(0,M,100)


	
	for t in xrange(M):
		Gamma,node,ko = [],[],[]
		for i in nodes:
			ocolor = solution[i]
			bb,ncolor = neighborcolor(i)
			new = set(solution) - ncolor
			if new:
				newcolor = list(new)
				for k in newcolor:
					if [i,k] in tabu:
						if [i,k] not in aspiration:
							continue
					g = gam(ocolor,k,Class)
					if Gamma != []:
						if g > Gamma:
							Gamma = g
							node = i
							ko = k
					else:
						Gamma = g
						node = i
						ko = k
		#print node,ko
		if Gamma == []:
			node = randrange(node_count)
			Class[solution[node]].remove(node)
			ko = max(solution) + 1
			tabu.append([node,ko])
			tabu.pop(0)
			if len(Class) < solution[node]:
				Class.append([node])
			else:
				Class[solution[node]].append(node)
		else:
			Class[solution[node]].remove(node)
			solution[node] = ko
			Class[ko].append(node)
			tabu.append([node,ko])
			tabu.pop(0)
			if Gamma > 0:
				s += Gamma
				star = solution[:]
				aspiration.append([node,ko])
				aspiration.pop(0)
		
		if t in AAA:
			print t


	#star = update(Class)
	# check 
	#Class = generateclass(solution)
	node_count = len(set(star))
	c = []
	for i in edges:
		temp = star[i[0]] - star[i[1]]
		c.append(temp)
	if 0 in c:
		a = 0
	else:
		a = 1



	# prepare the solution in the specified output format
	output_data = str(node_count) + ' ' + str(a) + '\n'
	output_data += ' '.join(map(str, star))

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

