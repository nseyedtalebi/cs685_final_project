from model import *
import sys
import snap
import time

if len(sys.argv)!=5:
	print("Improper usage, call as",sys.argv[0]," alpha_value zeta_value iteration_number iteration_times.\n")
	sys.exit(1)


alpha=float(sys.argv[1])
zeta=float(sys.argv[2])
	
iterNumber=sys.argv[3]
iters=int(sys.argv[4])


current_seed=6


gen=snap.TRnd()
head='outputs\\'+iterNumber
if int(iterNumber)==0:
	head='outputs\\'

for index in range(0,iters):
	print('Iteration',index)
	
	'''
	ER_Nodes=10000
	ER_Edges=ER_Nodes*5
	#Single instance for ER graph.
	gen.PutSeed(current_seed)
	graphER=Graph(alpha,zeta)
	ER=snap.GenRndGnm(snap.PUNGraph,ER_Nodes,ER_Edges,False,gen)
	for it in ER.Edges():
		graphER.AddEdge(it.GetSrcNId(),it.GetDstNId())
	#Choose random infected.
	infected=random.randint(0,len(graphER.verts))
	graphER.states[infected]=(0,1,0,0)
	print("ER graph:")
	start=time.time()
	graphER.do_simulation(10000,infected)
	end=time.time()
	print("Simulation took",(end-start))

	print( "Writing to output:")
	
	with open(head+"EROutput"+str(index)+".txt",'w+') as fp:
		header=str(ER_Nodes)+','+str(ER_Edges)+'\n'
		fp.write(header)
		timesteps=graphER.values_at_each
		for i in range(0,len(timesteps)):
			line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
			fp.write(line)
	print( "Finished outputting\n")
		
	WS_Nodes=1000
	WS_Edges=6
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
	graphWS.do_simulation(10000,infected)
	end=time.time()
	print "Simulation took",(end-start)


	print "Writing to output:"
	with open(head+"WSOutput"+str(index)+".txt",'w+') as fp:
		header=str(WS_Nodes)+','+str(WS_Edges)+'\n'
		fp.write(header)
		timesteps=graphWS.values_at_each
		for i in range(0,len(timesteps)):
			line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
			fp.write(line)
	print "Finished outputting\n"
	'''
	BA_Nodes=500000
	BA_Edge=6
	#Single instance for WS graph.
	gen.PutSeed(current_seed)
	graphBA=Graph(alpha,zeta)
	BA=snap.GenPrefAttach(BA_Nodes,BA_Edge,gen)
	for it in BA.Edges():
		graphBA.AddEdge(it.GetSrcNId(),it.GetDstNId())
	#Choose random infected.
	infected=random.randint(0,len(graphBA.verts))
	graphBA.states[infected]=(0,1,0,0)
	print( "BA graph:")
	start=time.time()
	graphBA.do_simulation(10000,infected)
	end=time.time()
	print( "Simulation took",(end-start))

	print( "Writing to output:")
	with open(head+"BAOutput"+str(index)+".txt",'w+') as fp:
		header=str(BA_Nodes)+','+str(BA_Edge)+'\n'
		fp.write(header)
		timesteps=graphBA.values_at_each
		for i in range(0,len(timesteps)):
			line=str(timesteps[i][0])+','+str(timesteps[i][1])+','+str(timesteps[i][2])+','+str(timesteps[i][3])+'\n'
			fp.write(line)
	print( "Finished outputting\n")
	