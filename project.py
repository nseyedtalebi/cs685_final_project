import sys
from random import randint

#according to the paper, (0,0,1) is S, (1,0,0) is B, (0,1,0) is F.

#Assuming undirected graphs:
class Graph:
	def __init__(self,forget,verify,alpha,beta):
		self.verts=set()
		self.states={}
		self.edges={}
		self.edgeNums=0
		self.alpha=alpha
		self.beta=beta
		self.pforget=forget
		self.pverify=verify
	def AddNode(self,index):
		if not index in self.verts:
			self.verts.add(index)
			self.edges[index]=set()
			self.states[index]=(0,0,1)
	def AddEdge(self,index1,index2):
		self.AddNode(index1)
		self.AddNode(index2)
		self.edges[index1].add(index2)
		self.edges[index2].add(index1)
		self.edgeNums+=1
	#returns the number of neighbors in each state.
	def neighborsStates(self,index):
		neighbors=self.edges[index]
		numF=0
		numB=0
		numS=0
		for adj in neighbors:
			result=self.states[adj]
			if result[0]==1:
				numB+=1
			elif result[1]==1:
				numF+=1
			else:
				numS+=1
		return (numB,numF,numS)	
	def probabilityB(self,index,fx,gx):
		return fx*self.states[index][2]+(1-self.pforget-self.pverify)*self.states[index][0]
	def probabilityF(self,index,fx,gx):
		return gx*self.states[index][2]+self.pverify*self.states[index][0]+(1-self.pforget)*self.states[index][1]		
	def probabilityS(self,index,fx,gx):
		return self.pforget*(self.states[index][0]+self.states[index][1])+(1-fx-gx)*self.states[index][2]	
	def getProbabilities(self,index):
		fx=self.function_fx(index)
		gx=self.function_gx(index)
		return (self.probabilityB(index,fx,gx),self.probabilityF(index,fx,gx),self.probabilityS(index,fx,gx))	
	def function_fx(self,index):
		currentNeighborStates=self.neighborsStates(index)
		if currentNeighborStates[0]==0 and currentNeighborStates[1]==0:
			return 0
		return self.beta*((currentNeighborStates[0]*(1+self.alpha))/( (currentNeighborStates[0]*(1+self.alpha)) + (currentNeighborStates[1]*(1-self.alpha)) ) )
	def function_gx(self,index):
		currentNeighborStates=self.neighborsStates(index)
		if currentNeighborStates[0]==0 and currentNeighborStates[1]==0:
			return 0
		return self.beta*((currentNeighborStates[1]*(1-self.alpha))/( (currentNeighborStates[0]*(1+self.alpha)) + (currentNeighborStates[1]*(1-self.alpha)) ) )	
	def do_simulation(self,amount_of_rounds):
		rounds=0
		while rounds<amount_of_rounds:
			next_states={}
			amounts={0:0,1:0,2:0}
			for vert in self.verts:
				probs=self.getProbabilities(vert)
				randChance=randint(0,100)/100
				index=0
				total=0
				while index<3 and total<randChance:
					total+=probs[index]
					if total>=randChance:
						break
					index+=1
				if index==3:
					index-=1
				next_state=(0,0,1)
				if index==0:
					next_state=(1,0,0)
				elif index==1:
					next_state=(0,1,0)
				next_states[vert]=next_state
				amounts[index]+=1
			self.states=next_states
			rounds+=1
			print("S:",amounts[2],"\tF:",amounts[1],"\tB:",amounts[0])
def Loadgraph(filename, fg, vf,alpha,beta):
	g=Graph(fg,vf,alpha,beta)
	with open(filename,'r') as fp:
		line=fp.readline()
		while line:
			if line[0]!='#':
				indicies=line.split('\t')
				g.AddEdge(int(indicies[0].strip()),int(indicies[1].strip()))
			line=fp.readline()
	return g
	
if len(sys.argv)!=6:
	print("Improper usage, call as",sys.argv[0],"graph_filename p_forget_value p_verify_value alpha_value beta_value\n")
	sys.exit(1)

pforget=float(sys.argv[2])
pverify=float(sys.argv[3])
alpha=float(sys.argv[4])
beta=float(sys.argv[5])
graph=Loadgraph(sys.argv[1],pforget,pverify,alpha,beta)
infected=randint(0,len(graph.verts))
graph.states[infected]=(1,0,0)
graph.do_simulation(1000)
#nif -> number of fact checker neighbors.
#nib -> number of believer neighbors.




