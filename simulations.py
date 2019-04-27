import sys
import time
import random
 
import snap
import seir

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

def run_simulation(input_graph,iterations):
	g = seir.Graph(alpha, zeta, input_graph)
	#Choose random infected.
	g.states[random.sample(g.verts,1)[0]] = (0,1,0,0)
	g.do_simulation(iterations)
	return g.values_at_each

num_runs = 100
ER_Nodes=10000
ER_Edges=40000
#Single instance for ER graph.
gen.PutSeed(current_seed)
er_runs = []
for run in range(0,num_runs):
	g = snap.GenRndGnm(snap.PUNGraph,ER_Nodes,ER_Edges,False,gen)
	er_runs.append(run_simulation(g,1000))
print er_runs
'''
WS_Nodes=50000
WS_Edges=1000
#Single instance for WS graph.
gen.PutSeed(current_seed)
graphWS=seir.Graph(alpha,zeta)
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
graphBA=seir.Graph(alpha,zeta)
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
'''