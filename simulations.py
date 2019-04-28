import sys
import time
import random
import pickle
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

import snap
import seir

alpha=0.9
zeta=0.02
cores = 4
current_seed=6
gen=snap.TRnd()
gen.PutSeed(6)

def amounts_add(x,y):
	return tuple([x[i]+y[i] for i in range(0,4)])

def run_simulation(input_graph,alpha,zeta,*args,**kwargs):
	g = seir.Graph(alpha, zeta, input_graph)
	#Choose random infected.
	infected = random.sample(g.verts,1)[0]
	g.states[infected] = (0,1,0,0)
	g.current_threshold[infected] = random.gauss(6,1)
	g.current_period[infected] = 0
	g.do_simulation(kwargs.get('iterations',1000))
	return g.values_at_each

def run_er_simulation(num_nodes,num_edges,alpha,zeta,*args,**kwargs):
	r = snap.GenRndGnm(snap.PUNGraph,num_nodes,num_edges,False,gen)
	return run_simulation(r,alpha,zeta,*args,**kwargs)

def run_ws_simulation(num_nodes,num_edges,alpha,zeta,*args,**kwargs):
	r = snap.GenSmallWorld(num_nodes,num_edges,0,gen)
	return run_simulation(r,alpha,zeta,*args,**kwargs)

def run_ba_simulation(num_nodes,num_edges,alpha,zeta,*args,**kwargs):
	r = snap.GenPrefAttach(num_nodes,num_edges,gen)
	return run_simulation(r,alpha,zeta,*args,**kwargs)

def estimate_r0(num_runs,sim_func,*args,**kwargs):
	runs = [sim_func(*args,**kwargs)[0][1] for run in range(0,num_runs)]
	return float(sum(runs))/float(len(runs))

def get_ensemble(num_runs,sim_func,*args,**kwargs):
	runs = [sim_func(*args,**kwargs) for run in range(0,num_runs)]
	totals = {}
	for run in runs:
		for timestep,amounts in run.items():
			if timestep in totals:
				totals[timestep].append(amounts)
			else:
				totals[timestep] = [amounts]
	avgd = {}
	for timestep in totals:
		totals_seir = reduce(amounts_add,totals[timestep],(0,0,0,0))
		num_pts = len(totals[timestep])
		avgd[timestep] = tuple(i/float(num_pts) for i in totals_seir)
	return avgd

def write_r0_estimates():
	num_runs = 50
	r0_er = {i*500:estimate_r0(num_runs,run_er_simulation,500,500*i,alpha,zeta,iterations=1) for i in range(1,20)}
	r0_ba = {i:estimate_r0(num_runs,run_ws_simulation,500,i,alpha,zeta,iterations=1) for i in range(1,20)}
	r0_ws = {i:estimate_r0(num_runs,run_er_simulation,500,i,alpha,zeta,iterations=1) for i in range(1,20)}
	with open('r0_er.pkl','w') as er:
		pickle.dump(r0_er,er)
	with open('r0_ba.pkl','w') as ba:
		pickle.dump(r0_ba,ba)
	with open('r0_ws.pkl','w') as ws:
		pickle.dump(r0_ws,ws)

num_nodes = 395
'''With 355 infected in the case study and a 90% secondary attack rate,
there were about 355/0.9 sufficent contacts'''
zeta_dublin = 3/395.0
write_r0_estimates()
#er_sims = get_ensemble(100,run_er_simulation,num_nodes,num_nodes*3,alpha,zeta_dublin)
#print er_sims




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