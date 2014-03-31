#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from random import shuffle

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
	return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def linking(series):
	links = [[series[-1],series[0]]]
	for i in xrange(len(series)-1):
		links.append([series[i],series[i+1]])
	return links

def solve_it(input_data):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = input_data.split('\n')

	nodeCount = int(lines[0])

	points = []
	for i in range(1, nodeCount+1):
		line = lines[i]
		parts = line.split()
		points.append(Point(float(parts[0]), float(parts[1])))

	def twodelta(a,b):
		oldlength1,oldlength2 = length(points[a[0]],points[a[1]]),length(points[b[0]],points[b[1]])
		newlength1,newlength2 = length(points[a[0]],points[b[0]]),length(points[a[1]],points[b[1]])
		delta = oldlength1 + oldlength2 - newlength1 - newlength2
		return delta


	# build a init trivial solution
	solution = range(0, nodeCount)
	#shuffle(solution)
	links = linking(solution)
	print 'linked'
	L = length(points[solution[-1]], points[solution[0]])
	for index in xrange(0, nodeCount-1):
		L += length(points[solution[index]], points[solution[index+1]])
	# visit the nodes in the order they appear in the file
	'''
	solution = [0]
	LL = set(range(1,nodeCount))
	l = 50
	for i in xrange(1,nodeCount):
		Q = points[solution[-1]]
		L,a = [],[]
		if len(LL) >100:
			k = list(LL)
			shuffle(k)
			s = k[:100]
		else:
			s = list(LL)
		shuffle(s)
		for t in s:
			P = points[t]
			if Q.x - l <= P.x <= Q.x + l and Q.y - l <= P.y <= Q.y + l :
				if L == []:
					L = length(P,Q)
					a = t
				elif L > length(P,Q):
					L = length(P,Q)
					a = t
		solution.append(a)
		LL -= set([a])
		if i%100 == 0:
			l+=1000
			print i
	print 'greedy done'
	'''
	t = 0
	while True:
		delta = []
		a,b=[],[]
		for i in xrange(nodeCount-2):
			for j in xrange(i+2,nodeCount):
				s = twodelta(links[i],links[j])
				if delta == [] or s >delta:
					delta = s
					a,b = i,j
		if round(delta,5) > 0:
			L -= delta
			temp = solution[a:b]
			solution[a:b] = temp[-1::-1]
			links = linking(solution)
		else:
			break
		t += 1
		if t %1 == 0:
			print t
	

	# calculate the length of the tour
	obj = length(points[solution[-1]], points[solution[0]])
	for index in range(0, nodeCount-1):
		obj += length(points[solution[index]], points[solution[index+1]])

	# prepare the solution in the specified output format
	output_data = str(obj) + ' ' + str(0) + '\n'
	output_data += ' '.join(map(str, solution))
	fre = open('D:\Users\sky\Documents\GitHub\discrete_opt\discrete optimization\\tsp\\result.txt','w')
	fff = open('D:\Users\sky\Documents\GitHub\discrete_opt\discrete optimization\\tsp\\resulttt.txt','w')
	fff.write(str(solution))
	fff.close()
	for i in xrange(nodeCount):
		fre.write(str(solution[i]))
		fre.write('\n')
	fre.close()

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
		print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'