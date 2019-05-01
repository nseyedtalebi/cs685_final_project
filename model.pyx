#Made by Joe Kaninberg
import random
#Unsure Aspects: X is a normally distributed random variable, but unsure as to the range. Defined best guess in do_simulation function.
#WS seems to be the slowest, most aberrant behavior.
#For the current test, alpha of 0.9 and zeta of 0.1.


#zeta is infectious mortality rate.
#alpha is immunity loss rate.


#Assuming undirected graphs:
cdef class Graph:
	cdef public set verts
	cdef public dict states
	cdef public dict edges
	cdef public dict values_at_each
	cdef public int edgeNums
	cdef public double alpha
	cdef public double zeta
	def __cinit__(self,alpha,zeta):
		self.verts=set()
		self.states={}
		self.edges={}
		self.edgeNums=0
		self.alpha=alpha
		self.zeta=zeta
		self.values_at_each={}
		
	cdef AddNode(self,int index):
		if not index in self.verts:
			self.verts.add(index)
			self.edges[index]=set()
			self.states[index]=(0,0,0,1)
	cpdef AddEdge(self,int index1,int index2):
		self.AddNode(index1)
		self.AddNode(index2)
		self.edges[index1].add(index2)
		self.edges[index2].add(index1)
		self.edgeNums+=1
	#checks adjacent nodes for infected.
	cdef neighborsStates(self,int index):
		st=self.states
		neighbors=self.edges[index]
		cdef int adj
		cdef int length=len(neighbors)
		for adj in neighbors:
			if st[adj][1]==1:
				return (0,1,0,0)
		return (0,0,0,0)	
	
	def do_simulation(self,int amount_of_rounds, int infected):
		cdef int rounds=0
		#reset discrete graph generation for random results.
		random.seed(None)
		cdef dict current_period={i:-1 for i in self.verts}
		cdef dict current_threshold={i:-1 for i in self.verts}
		#Based on slides assuming incubation period is only 10-12 days, to add more add them into the list.
		cdef list incubation_days=[10,11,12]
		#Assuming the same for the infection days.
		cdef list infection_days=[5,6]
		current_period[infected]=0
		current_threshold[infected]=infection_days[random.randint(0,len(infection_days)-1)]
		st=self.states
		vt=self.verts
		cdef dict amounts
		cdef dict next_states
		cdef double alpha=self.alpha
		cdef double zeta=self.zeta
		vals=self.values_at_each
		cdef int removed=0
		cdef list removeNext=[]
		#print(self.alpha,self.zeta,amount_of_rounds)
		while rounds<amount_of_rounds:
			next_states={}
			#The amount of nodes in each state. From Left to right for indicies, R:0,I:1,E:2,S:3.
			amounts={1:0,2:0,3:0}
			
			for vert in vt:
				randChance=float(random.randint(0,100))/100.0
				#S
				if st[vert][3]==1:
					neighbors=self.neighborsStates(vert)
					#Chance to transition from S to E.
					if neighbors[1]>0 and randChance<=alpha:
						next_states[vert]=(0,0,1,0)
						amounts[2]+=1
						current_period[vert]=0
						#Generate the incubation time threshold X sub e.
						current_threshold[vert]=incubation_days[random.randint(0,len(incubation_days)-1)]
					#Else remain in S.
					else:
						next_states[vert]=(0,0,0,1)
						amounts[3]+=1
				#E
				elif st[vert][2]==1:
					#check the probability for transition to E.
					if current_period[vert]==current_threshold[vert]:
						current_period[vert]=0
						next_states[vert]=(0,1,0,0)
						#Generate the infection time threshold X sub i.
						current_threshold[vert]=infection_days[random.randint(0,len(infection_days)-1)]
						amounts[1]+=1
						continue
					else:
						next_states[vert]=(0,0,1,0)
						amounts[2]+=1
					#increment tau sub e.
					current_period[vert]+=1
				#I
				elif st[vert][1]==1:
					#Chance of death/recovery occuring.
					if randChance<=zeta or current_period[vert]==current_threshold[vert]:
						next_states[vert]=(1,0,0,0)
						removeNext.append(vert)
						continue
					else:
						next_states[vert]=(0,1,0,0)
						amounts[1]+=1
					#increment tau sub i.
					current_period[vert]+=1
				#R remain in current state.
			removed+=len(removeNext)
			for item in removeNext:
				vt.remove(item)
			removeNext=[]
			for item in next_states:
				self.states[item]=next_states[item]
			st=self.states
			vals[rounds]=(amounts[3],amounts[2],amounts[1],removed)
			rounds+=1
			print rounds,"\tS:",amounts[3],"  E:",amounts[2],"  I:",amounts[1],"  R:",removed
			#Break if every node is recovered/dead or stranded.
			if amounts[3]==len(vt):
				break
def Loadgraph(filename,alpha,zeta):
	g=Graph(alpha,zeta)
	with open(filename,'r') as fp:
		line=fp.readline()
		while line:
			if line[0]!='#':
				indicies=line.split('\t')
				g.AddEdge(int(indicies[0].strip()),int(indicies[1].strip()))
			line=fp.readline()
	return g
	








