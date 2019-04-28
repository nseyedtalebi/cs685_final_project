import sys
import random
import time
import itertools
from multiprocessing.dummy import Pool as ThreadPool
from math import floor

import snap

#https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def sum_dicts(x,y):
	for key,val in x.items():
		if key in y:
			y[key]+=val
		else:
			y[key]
	return y
#zeta is infectious mortality rate.
#alpha is immunity loss rate.
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
		self.current_period={i:-1 for i in self.verts}
		self.current_threshold={i:-1 for i in self.verts}

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
		
		amounts={0:0,1:0,2:0,3:0,4:0}
		while rounds<amount_of_rounds:
			#The amount of nodes in each state. From Left to right for indicies, R:0,I:1,E:2,S:3.
			self.states, amounts = self._update_states(self.verts)
			self.values_at_each[rounds]=(amounts[3],amounts[2],amounts[1],amounts[0])
			rounds+=1
			#print rounds,"\tS:",amounts[3],"  E:",amounts[2],"  I:",amounts[1],"  R:",amounts[0]
			#Break if every node is recovered/dead or stranded.
			if rounds > 70:
				print "ay"
			if amounts[0]+amounts[3]==len(self.verts):
				break

	def do_simulation_threaded(self,amount_of_rounds, pool_size = 8):
		rounds=0
		#reset discrete graph generation for random results.
		random.seed(None)
		
		amounts={0:0,1:0,2:0,3:0,4:0}
		while rounds<amount_of_rounds:
			#The amount of nodes in each state. From Left to right for indicies, R:0,I:1,E:2,S:3.
			pool = ThreadPool(pool_size)
			#vert_chunks = chunks(list(self.verts),int(floor(len(self.verts)/pool_size)))
			res = pool.map(self._update_states,self.verts,int(floor(len(self.verts)/pool_size)))
			pool.close()
			pool.join()
			next_states = [r[0] for r in res]
			partial_amounts = [r[1] for r in res]
			self.states = reduce(merge_dicts,next_states,{})
			amounts = reduce(sum_dicts,partial_amounts,{0:0,1:0,2:0,3:0,4:0})
			self.values_at_each[rounds]=(amounts[3],amounts[2],amounts[1],amounts[0])
			rounds+=1
			#print rounds,"\tS:",amounts[3],"  E:",amounts[2],"  I:",amounts[1],"  R:",amounts[0]
			#Break if every node is recovered/dead or stranded.
			if amounts[0]+amounts[3]==len(self.verts):
				break

	def _update_states(self,verts):
		next_states={}
		amounts={0:0,1:0,2:0,3:0,4:0}
		for vert in verts:
			randChance=random.random()
			#S
			if self.states[vert]==(0,0,0,1):
				#Chance to transition from S to E.
				if self.InfectiousNeighbors(vert) and randChance<=self.alpha:
					next_states[vert]=(0,0,1,0)
					amounts[2]+=1
					self.current_period[vert]=0
					#Generate the incubation time threshold X sub e.
					e_days = random.gauss(11,2)
					self.current_threshold[vert]= e_days
				#Else remain in S.
				else:
					next_states[vert]=(0,0,0,1)
					amounts[3]+=1
			#E
			elif self.states[vert]==(0,0,1,0):
				#check the probability for transition to E.
				if self.current_period[vert] >= self.current_threshold[vert] and \
				self.current_threshold[vert] > 0:
					self.current_period[vert]=0
					next_states[vert]=(0,1,0,0)
					#Generate the infection time threshold X sub i.
					i_days  = random.gauss(6,1)
					self.current_threshold[vert]= i_days
					amounts[1]+=1
					continue
				else:
					next_states[vert]=(0,0,1,0)
					amounts[2]+=1
				#increment tau sub e.
				self.current_period[vert]+=1
			#I
			elif self.states[vert]==(0,1,0,0):
				#Chance of death/recovery occuring.
				if randChance<=self.zeta or \
				(self.current_period[vert] >= self.current_threshold[vert] and \
				self.current_threshold[vert] > 0):
					self.current_period[vert]=0
					next_states[vert]=(1,0,0,0)
					amounts[0]+=1
					continue
				else:
					next_states[vert]=(0,1,0,0)
					amounts[1]+=1
				#increment tau sub i.
				self.current_period[vert]+=1
			#R remain in current state.
			elif self.states[vert]==(1,0,0,0):
				amounts[0]+=1
				next_states[vert]=(1,0,0,0)
		return next_states,amounts

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
	
