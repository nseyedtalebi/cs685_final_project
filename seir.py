import sys
import random
import time

import snap

#Unsure Aspects: X is a normally distributed random variable, but unsure as to the range. Defined best guess in do_simulation function.
#WS seems to be the slowest, most aberrant behavior.
#For the current test, alpha of 0.9 and zeta of 0.1.


#zeta is infectious mortality rate.
#alpha is immunity loss rate.


#Assuming undirected graphs:
class Graph:
	def __init__(self,alpha,zeta,snap_graph=None):
		self.verts=set()
		self.states={}
		self.edges={}
		self.edgeNums=0
		self.alpha=alpha
		self.zeta=zeta
		#Used to store the number of nodes in each state at each timestep.
		self.values_at_each={}
		if snap_graph:
			for it in snap_graph.Edges():
				self.AddEdge(it.GetSrcNId(),it.GetDstNId())

	def AddNode(self,index):
		if not index in self.verts:
			self.verts.add(index)
			self.edges[index]=set()
			self.states[index]=(0,0,0,1)
	def AddEdge(self,index1,index2):
		self.AddNode(index1)
		self.AddNode(index2)
		self.edges[index1].add(index2)
		self.edges[index2].add(index1)
		self.edgeNums+=1
	#returns the number of neighbors in each state.
	def InfectiousNeighbors(self,index):
		for adj in self.edges[index]:
			if self.states[adj][1] == 1:
				return True
		return False
	
	def do_simulation(self,amount_of_rounds):
		rounds=0
		#reset discrete graph generation for random results.
		random.seed(None)
		current_period={i:-1 for i in self.verts}
		current_threshold={i:-1 for i in self.verts}

		while rounds<amount_of_rounds:
			next_states={}
			#The amount of nodes in each state. From Left to right for indicies, R:0,I:1,E:2,S:3.
			amounts={0:0,1:0,2:0,3:0,4:0}
			for vert in self.verts:
				randChance=random.random()
				#S
				if self.states[vert]==(0,0,0,1):
					#Chance to transition from S to E.
					if self.InfectiousNeighbors(vert) and randChance<=self.alpha:
						next_states[vert]=(0,0,1,0)
						amounts[2]+=1
						current_period[vert]=0
						#Generate the incubation time threshold X sub e.
						current_threshold[vert]=random.gauss(11,2)
					#Else remain in S.
					else:
						next_states[vert]=(0,0,0,1)
						amounts[3]+=1
				#E
				elif self.states[vert]==(0,0,1,0):
					#check the probability for transition to E.
					if current_period[vert] >= current_threshold[vert] and \
					current_threshold[vert] > 0:
						current_period[vert]=0
						next_states[vert]=(0,1,0,0)
						#Generate the infection time threshold X sub i.
						current_threshold[vert]=random.gauss(6,1)
						amounts[1]+=1
						continue
					else:
						next_states[vert]=(0,0,1,0)
						amounts[2]+=1
					#increment tau sub e.
					current_period[vert]+=1
				#I
				elif self.states[vert]==(0,1,0,0):
					#Chance of death/recovery occuring.
					if randChance<=self.zeta or \
					(current_period[vert] >= current_threshold[vert] and \
					current_threshold[vert] > 0):
						next_states[vert]=(1,0,0,0)
						amounts[0]+=1
						continue
					else:
						next_states[vert]=(0,1,0,0)
						amounts[1]+=1
					#increment tau sub i.
					current_period[vert]+=1
				#R remain in current state.
				elif self.states[vert]==(1,0,0,0):
					amounts[0]+=1
					next_states[vert]=(1,0,0,0)
			self.states=next_states
			self.values_at_each[rounds]=(amounts[3],amounts[2],amounts[1],amounts[0])
			rounds+=1
			#print rounds,"\tS:",amounts[3],"  E:",amounts[2],"  I:",amounts[1],"  R:",amounts[0]
			#Break if every node is recovered/dead or stranded.
			if amounts[0]+amounts[3]==len(self.verts):
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
	
