input_data_file = open('D:\Users\sky\Documents\GitHub\discrete_opt\discrete optimization\coloring\data\gc_50_3', 'r')
input_data = ''.join(input_data_file.readlines())
input_data_file.close()
lines = input_data.split('\n')
first_line = lines[0].split()
node_count = int(first_line[0])
edge_count = int(first_line[1])
edges = []
for i in range(1, edge_count + 1):
    line = lines[i]
    parts = line.split()
    edges.append((int(parts[0]), int(parts[1])))

neighbors = []
for i in xrange(node_count):
  	temp = set([i])
  	for k in edges:
  		if i in k:
  			temp|= set(k)
   	neighbors.append(temp)

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



solution = [x for x in xrange(node_count)]
Class = generateclass(solution)

star = solution[:]
s = ff(Class)
tabu = []
tabu.append(star[:])
aspiration = []
colorn = len(Class)

Delta,ci,cj = [],[],[]

A,B = Class[ci],Class[cj]
At,Bt = sswap(A,B)
Class[ci],Class[cj] = At,Bt
solution = updatesolution(At,Bt,ci,cj,solution)
tempsolution = solution[:]
tabu.append(tempsolution)
if Delta >0:
	s += Delta
	star = tempsolution
   	aspiration = star
   	TClass = Class[:]



#Class = generateclass(solution)
    #print 'Class done'
    #global s
    #s = ff(Class)
    #print 's done'
    #greedy with swap
    #t = 1
    #for i in nodes:
    #    print 'start',t
    #    s = coloring(i,s,Class)
    #    print t,'done'
    #    t+=1
        #s = swap(Class,s)
        #Class = generateclass(solution)
        #solution = update(Class)
    #teclass = Class[:]   
    '''
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
    '''











   	'''
    				if Delta != []:
    					if d > Delta:
    						ci = i
    						cj = j
    						Delta = d
    						#Class[i] = at
    						#Class[j] = bt
    						#TClass = Class[:]
    				else:
    					Delta = d
    					ci = i
    					cj = j
    					#Class[i] = at
    					#Class[j] = bt
    					#TClass = Class[:]
    				'''



    				test = solution[:]
    				tsolution = updatesolution(aset,bset,i,j,test)
    				if tsolution in tabu:
    					if tsolution != aspiration:
    						continue
    				#d = delta(a,b,aset,bset)		
    				#at,bt = sswap(a,b)
    				print i,j


    				    def swap(Class,s):
        while True:
            modify = 0
            n = len(Class)
            nodes = [x for x in xrange(n)]
            shuffle(nodes)
            for i in xrange(n):
                for j in xrange(i+1,n):
                    a = Class[nodes[i]]
                    a = a[:]
                    b = Class[nodes[j]]
                    b = b[:]
                    if a and b:
                        aset,bset = foo(a,b)
                        if aset:
                            at = (set(a)-aset)|bset
                            bt = (set(b)-bset)|aset
                            Class[nodes[i]] = list(at)
                            Class[nodes[j]] = list(bt)                          
                        else:
                            at = set(a)|set(b)
                            Class[nodes[i]] = list(at)
                            Class[nodes[j]] = []
                        sn = ff(Class)
                        if sn > s:
                            s = sn
                            modify = 1
                            for k in Class[nodes[i]]:
                                solution[k] = i
                            for k in Class[nodes[j]]:
                                solution[k] = j
                        else:
                            Class[nodes[i]] = a
                            Class[nodes[j]] = b
            if modify == 0:
                break
        return s


    def update(Class):
        while Class.count([]):
            Class.remove([])
        solution = [0]*node_count
        for color in xrange(len(Class)):
            for node in Class[color]:
                solution[node] = color
        return solution


    def neighborcolor(node):
        color = []
        domain = list(set(neighbors[node]))
        for neighbor in domain:
            color.append(solution[neighbor])
        ncolor = set(color)
        return len(ncolor),ncolor

    def coloring(node,s,Class):
        m,ncolor = neighborcolor(node)
        colors = set(solution) - ncolor
        #Class = generateclass(solution)
        #s = f(Class)
        nodecolor = solution[node]
        if colors:
            for tryc in list(colors):
                at = Class[nodecolor]
                at = at[:]
                bt = Class[tryc]
                bt = bt[:]
                #tclass = generateclass(solution)
                Class[nodecolor].remove(node)
                Class[tryc].append(node)
                badn,sn = f(Class)
                if sn < s:
                    s = sn
                    nodecolor = tryc                    
                    solution[node] = nodecolor
                else:
                    Class[nodecolor] = at
                    Class[tryc] = bt
        else:
            Class[nodecolor].remove(node)
            nodecolor = m
            solution[node] = nodecolor
            Class.append([node])
            badn,s = f(Class)
        return badn,s

    def Bad_edge(Class):
        Bad = []
        for color in Class:
            bad = []
            for edge in edges:
                if set(edge) <= set(color):
                    bad.append(edge)
            Bad.append(bad)
        return Bad

    def bad_count(Bad):
        bad = []
        for b in Bad:
            bad.extend(b)
        return bad,len(bad)        

        if a and b:
    				at,bt = sswap(a,b)
    				test = solution[:]
    				tsolution = updatesolution(at,bt,i,j,test)
    				if tsolution in tabu:
    					if tsolution not in aspiration:
    						continue
    				d = delta(a,b,at,bt)
    				if Delta != []:
    					if d > Delta:
    						ci = i
    						cj = j
    						Delta = d
    				else:
    					Delta = d
    					ci = i
    					cj = j



    '''
    for t in xrange(L):
    	Delta = []
    	#ci,cj = [],[]
    	nei = []
    	for i in xrange(0,colorn-1):
    		for j in xrange(i+1,colorn):
    			a,b = Class[i],Class[j]
    			if a and b:			    				
    				at,bt = sswap(a,b)
    				test = solution[:]
    				tsolution = updatesolution(at,bt,i,j,test)
    				if tsolution in tabu:
    					if tsolution not in aspiration:
    						continue
    				#d = delta(a,b,at,bt)
    				nei.append([i,j])
    				
    				if Delta != []:
    					if d > Delta:
    						ci = i
    						cj = j
    						Delta = d
    				else:
    					Delta = d
    					ci = i
    					cj = j
    				
    	k = len(nei)
    	ra = randrange(k)
    	ci = nei[ra][0]
    	cj = nei[ra][1]
    	
    	if ci == []:
    		tabu.append([])
    		tabu.pop(0)
    		continue
    	
    	A,B = Class[ci],Class[cj]
    	At,Bt = sswap(A,B)
    	Class[ci],Class[cj] = At,Bt
    	Delta = delta(A,B,At,Bt)
    	solution = updatesolution(At,Bt,ci,cj,solution)
    	tempsolution = solution[:]
    	tabu.append(tempsolution)    	
    	tabu.pop(0)
    	if Delta >0:
    		s += Delta
    		star = tempsolution
    		aspiration.append(star)
    		aspiration.pop(0)
    		TClass = Class[:]
    	if t in AAA:
    		print t
		
	'''