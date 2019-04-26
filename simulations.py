import sys
import time

import snap 

import seir_snap

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


ER_Nodes=10000
ER_Edges=40000
#Single instance for ER graph.
gen.PutSeed(current_seed)
graphER=snap.GenRndGnm(snap.PUNGraph,ER_Nodes,ER_Edges,False,gen)
#Choose random infected.
states = {}#snap.TIntH()
for node in graphER.Nodes():
	states[node.GetId()] = 1
states[graphER.GetRndNId(gen)]=4
print "ER graph:"
start=time.time()
result = seir_snap.do_simulation(graphER,100,states,alpha,zeta)
end=time.time()
print "Simulation took",(end-start)
print result