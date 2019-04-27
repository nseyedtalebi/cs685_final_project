import sys
import time
import random
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import timeit

import snap
import seir

if len(sys.argv)!=3:
	print "Improper usage, call as",sys.argv[0]," alpha_value zeta_value\n"
	sys.exit(1)


alpha=float(sys.argv[1])
zeta=float(sys.argv[2])
	
cores = 4
current_seed=6
#To seed the graph of the same number, push the number to gen then generate the graph.	
#GenRndGnm for ER graph. GenRndGnm(snap.PNGraph,node_nums,edge_nums,false,TRnd for random number generation).
#GenSmallWorld for WS graph. GenSmallWorld(node_nums,avgerage_degree,rewire probability,TRnd for random number generation)
#GenPrefAttach for BA graph. GenPrefAttach(node_nums, NodeOutDegree,TRnd for random number generation)


def run_simulations_threaded(func,cores,num_runs):
	pool = ThreadPool(cores)
	runs = pool.map(er_sim,range(0,num_runs))
	pool.close()
	pool.join()
	return runs

def run_er_simulation(num_nodes,num_edges,alpha,zeta,*args,**kwargs):
	gen=snap.TRnd()
	gen.PutSeed(6)
	input_graph = snap.GenRndGnm(snap.PUNGraph,num_nodes,num_edges,False,gen)
	g = seir.Graph(alpha, zeta, input_graph)
	#Choose random infected.
	g.states[random.sample(g.verts,1)[0]] = (0,1,0,0)
	g.do_simulation(kwargs.get('iterations',1000))
	return g.values_at_each

def estimate_r0_er(tolerance=0.01):
	change = 99999
	r0 = 0
	runs = []
	while abs(change) > tolerance:
		#get number of exposed people from first (and only) timestep of sim
		runs.append(run_er_simulation(1000,4000,alpha,zeta,iterations=1)[0][1])
		r0_new = sum(runs)/len(runs)
		change = r0_new - r0
		r0 = r0_new
	return r0

print estimate_r0_er(0.001)



#er_sim = partial(run_er_simulation,1000,4000,alpha,zeta,iterations=1000)
#er_runs = run_simulations_threaded(er_sim,4,10)
#will send an extra argument to er_sim that I ignore
#Feels unpythonic but does it work?

#print er_runs
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