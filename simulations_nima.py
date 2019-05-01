#Written by Nima, based on examples from Joe
import sys
import time
import random
import pickle
from datetime import datetime
import cProfile
from collections import defaultdict

import snap
import seir_nima
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
alpha=0.9
zeta=0.02
cores = 4
current_seed=6
gen=snap.TRnd()
gen.PutSeed(6)
zeta_dublin = 3/395.0

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

def run_ws_simulation(num_nodes,num_edges,rewire_prob,alpha,zeta,*args,**kwargs):
	r = snap.GenSmallWorld(num_nodes,num_edges,rewire_prob,gen)
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
	num_runs = 100
	r0_er = {i*500:estimate_r0(num_runs,run_er_simulation,500,500*i,alpha,zeta,iterations=1) for i in range(1,20)}
	r0_ba = {i:estimate_r0(num_runs,run_ba_simulation,500,i,alpha,zeta,iterations=1) for i in range(1,20)}
	r0_ws_deg = {i:estimate_r0(num_runs,run_ws_simulation,500,i,0,alpha,zeta,iterations=1) for i in range(1,20)}
	r0_ws_beta = {i:estimate_r0(num_runs,run_ws_simulation,500,12,i*0.1,alpha,zeta,iterations=1) for i in range(0,11)}
	with open('r0_er.pkl','w') as er:
		pickle.dump(r0_er,er)
	with open('r0_ba.pkl','w') as ba:
		pickle.dump(r0_ba,ba)
	with open('r0_ws_deg.pkl','w') as ws_deg:
		pickle.dump(r0_ws_deg,ws_deg)
	
	with open('r0_ws_beta.pkl','w') as ws_beta:
		pickle.dump(r0_ws_beta,ws_beta)

def write_sim_results(results,filename='sim_output_'+datetime.strftime(datetime.now(),'%Y%m%d_%H%M%S')):
	with open(filename,'w') as fp:
		for i in results:
			line=str(results[i][0])+','+str(results[i][1])+','+str(results[i][2])+','+str(results[i][3])+'\n'
			fp.write(line)

def mse(gt_dict,ts_dict):
	gt = []
	ts = []
	for key,value in gt_dict.items():
		gt.append(value)
		if key in ts_dict:
			ts.append(ts_dict[key])
		else:
			ts.append(0.0)
	return mean_squared_error(gt,ts)

def get_infectious_by_week(sim_results):
	i_by_week = defaultdict(lambda x:0.0)
	for day in sim_results:
		if day % 7 == 0 and day > 0:
			i_by_week[(day/7)] = sim_results[day][2]
	return i_by_week

def load_dublin_case_data():
	dublin = {}
	with open('dublin_2000_measles.txt','r') as inf:
		inf.readline()#discard header
		for line in inf:
			r = line.strip().split('\t')
			dublin[int(r[0])]=int(r[1])
	return dublin

def get_mse_different_methods(num_nodes,ensemble_size,write_output=True):
	dublin = load_dublin_case_data()
	mses = defaultdict(dict)
	for i in range(1,20):
		arg_lists = {'er':(ensemble_size,run_er_simulation,num_nodes,num_nodes*i,alpha,zeta_dublin),
		'ba':(ensemble_size,run_ba_simulation,num_nodes,i,alpha,zeta_dublin),
		'ws':(ensemble_size,run_ws_simulation,num_nodes,i,0,alpha,zeta_dublin)}	
		for simtype,arg_list in arg_lists.items():
			sims = get_ensemble(*arg_list)
			mses[simtype][i] = mse(dublin,get_infectious_by_week(sims))
	if write_output:
		with open('mses.pkl','w') as outf:
			pickle.dump(mses,outf)
	return mses

def run_best_model():
	num_nodes = 395
	ensemble_size = 10000
	'''With 355 infected in the case study and a 90% secondary attack rate,
	there were about 355/0.9 sufficent contacts'''

	dublin = load_dublin_case_data()
	er_mse = {}
	#22: 831.1648814579835
	er_runs = get_ensemble(ensemble_size,run_er_simulation,num_nodes,int(num_nodes*(22/20)),alpha,zeta_dublin)
	with open('best_fit.pkl','w') as f:
		pickle.dump(er_runs,f)

#TODO:
'''
-add lines to mark acceptable r0 values for r0 estimates
-once best params are found, run model with high number of sims to produce smooth output for figures
-plot ground truth data from case study for figures
dublin = load_dublin_case_data()
er_mse = {}
#22: 831.1648814579835
for i in range (20,24):
	er_runs = get_ensemble(ensemble_size,run_er_simulation,num_nodes,int(num_nodes/20)*i,alpha,zeta_dublin)
	er_mse[i] = mse(dublin,get_infectious_by_week(er_runs))
print er_mse
'''

#keys,vals = seir.dict_results_to_lists(dublin)
#plt.plot(keys,vals)
#plt.show()

#er_sims = get_ensemble(10,run_er_simulation,num_nodes,num_nodes*3,alpha,zeta_dublin)
#print mse(dublin,get_infectious_by_week(er_sims))

#write_sim_results(i_by_week,'i_by_week.csv')
#print i_by_week






#write_sim_results(er_sims,filename='er_sim.csv')





#er_sim = partial(run_er_simulation,1000,4000,alpha,zeta,iterations=1000)
#er_runs = run_simulations_threaded(er_sim,4,10)
#will send an extra argument to er_sim that I ignore
#Feels unpythonic but does it work?