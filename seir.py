import sys
import random
import snap
import time
#Unsure Aspects: X is a normally distributed random variable, but unsure as to the range. Defined best guess in do_simulation function.
#WS seems to be the slowest, most aberrant behavior.
#For the current test, alpha of 0.9 and zeta of 0.1.


#zeta is infectious mortality rate.
#alpha is immunity loss rate.


#Assuming undirected graphs:
class Graph:
	def __init__(self,alpha,zeta):
		self.verts=set()
		self.states={}
		self.edges={}
		self.edgeNums=0
		self.alpha=alpha
		self.zeta=zeta
		#Used to store the number of nodes in each state at each timestep.
		self.values_at_each={}
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
	def neighborsStates(self,index):
		neighbors=self.edges[index]
		numR=0
		numI=0
		numE=0
		numS=0
		for adj in neighbors:
			result=self.states[adj]
			if result[0]==1:
				numR+=1
			elif result[1]==1:
				numI+=1
			elif result[2]==1:
				numE+=1
			else:
				numS+=1
		return (numR,numI,numE,numS)	
	
	def do_simulation(self,amount_of_rounds):
		rounds=0
		#reset discrete graph generation for random results.
		random.seed(None)
		current_period={i:-1 for i in self.verts}
		current_threshold={i:-1 for i in self.verts}
		#Based on slides assuming incubation period is only 10-12 days, to add more add them into the list.
		incubation_days=[10,11,12]
		#Assuming the same for the infection days.
		infection_days=[5,6]
		while rounds<amount_of_rounds:
			next_states={}
			#The amount of nodes in each state. From Left to right for indicies, R:0,I:1,E:2,S:3.
			amounts={0:0,1:0,2:0,3:0,4:0}
			for vert in self.verts:
				randChance=float(random.randint(0,100))/100.0
				#S
				if self.states[vert]==(0,0,0,1):
					neighbors=self.neighborsStates(vert)
					#Chance to transition from S to E.
					if neighbors[1]>0 and randChance<=self.alpha:
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
				elif self.states[vert]==(0,0,1,0):
					#check the probability for transition to E.
					if randChance<=(current_period[vert]/current_threshold[vert]):
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
				elif self.states[vert]==(0,1,0,0):
					#Chance of death/recovery occuring.
					if randChance<=self.zeta+(current_period[vert]/current_threshold[vert]):
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
			print rounds,"\tS:",amounts[3],"  E:",amounts[2],"  I:",amounts[1],"  R:",amounts[0]
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
	
if len(sys.argv)!=3:
	print "Improper usage, call as",sys.argv[0]," alpha_value zeta_value\n"
	sys.exit(1)


alpha=float(sys.argv[1])
zeta=float(sys.argv[2])
	
current_seed=6
#To seed the graph of the same number, push the number to gen then generate the graph.	
#GenRndGnm for ER graph. GenRndGnm(snap.PNGraph,node_nums,edge_nums,false,TRnd for random number generation).
#GenSmallWorld for WS graph. GenSmallWorld(node_nums,avgerage_degree,rewire probability,TRnd for random number generation)
#GenPrefAttach for BA graph. GenPrefAttach(node_nums, NodeOutDegree,TRnd for random number generation)


gen=snap.TRnd()


ER_Nodes=100000
ER_Edges=600000
#Single instance for ER graph.
gen.PutSeed(current_seed)
graphER=Graph(alpha,zeta)
ER=snap.GenRndGnm(snap.PUNGraph,ER_Nodes,ER_Edges,False,gen)
for it in ER.Edges():
	graphER.AddEdge(it.GetSrcNId(),it.GetDstNId())
#Choose random infected.
infected=random.randint(0,len(graphER.verts))
graphER.states[infected]=(0,1,0,0)
print "ER graph:"
start=time.time()
graphER.do_simulation(10000)
end=time.time()
print "Simulation took",(end-start)

print "Writing to output:"
with open("EROutput.txt",'w+') as fp:
	header=str(ER_Nodes)+','+str(ER_Edges)+'\n'
	fp.write(header)
	timesteps=graphER.values_at_each
	for i in range(0,len(timesteps)):
		line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
		fp.write(line)
print "Finished outputting\n"
		
		
WS_Nodes=50000
WS_Edges=1000
#Single instance for WS graph.
gen.PutSeed(current_seed)
graphWS=Graph(alpha,zeta)
WS=snap.GenSmallWorld(WS_Nodes,WS_Edges,0,gen)
for it in WS.Edges():
	graphWS.AddEdge(it.GetSrcNId(),it.GetDstNId())
#Choose random infected.
infected=random.randint(0,len(graphWS.verts))
graphWS.states[infected]=(0,1,0,0)
print "WS graph:"
start=time.time()
graphWS.do_simulation(10000)
end=time.time()
print "Simulation took",(end-start)


print "Writing to output:"
with open("WSOutput.txt",'w+') as fp:
	header=str(WS_Nodes)+','+str(WS_Edges)+'\n'
	fp.write(header)
	timesteps=graphWS.values_at_each
	for i in range(0,len(timesteps)):
		line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
		fp.write(line)
print "Finished outputting\n"



BA_Nodes=100000
BA_Edge=10
#Single instance for WS graph.
gen.PutSeed(current_seed)
graphBA=Graph(alpha,zeta)
BA=snap.GenPrefAttach(BA_Nodes,BA_Edge,gen)
for it in BA.Edges():
	graphBA.AddEdge(it.GetSrcNId(),it.GetDstNId())
#Choose random infected.
infected=random.randint(0,len(graphBA.verts))
graphBA.states[infected]=(0,1,0,0)
print "BA graph:"
start=time.time()
graphBA.do_simulation(10000)
end=time.time()
print "Simulation took",(end-start)

print "Writing to output:"
with open("BAOutput.txt",'w+') as fp:
	header=str(BA_Nodes)+','+str(BA_Edge)+'\n'
	fp.write(header)
	timesteps=graphBA.values_at_each
	for i in range(0,len(timesteps)):
		line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
		fp.write(line)
print "Finished outputting\n"








