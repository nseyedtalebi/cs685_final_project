import random

import snap

def check_neighbors(n,states):
	for nid in n.GetOutEdges():
		if states[nid] == 4:
			return True
	return False

def do_simulation(g,amount_of_rounds,states,alpha,zeta):
	rounds=0
	#reset discrete graph generation for random results.
	random.seed(None)
	current_period = {}
	current_threshold = {}
	for i in g.Nodes():
		current_period[i.GetId()] = 0
		current_threshold[i.GetId()] = 0
	values_at_each = {}
	#Based on slides assuming incubation period is only 10-12 days, to add more add them into the list.
	incubation_days=[10,11,12]
	#Assuming the same for the infection days.
	infection_days=[5,6]
	amounts = {}#
	#Start with |g| in compartment S
	amounts['S'] = g.GetNodes()
	amounts['E'] = 0
	amounts['I'] = 0
	amounts['R'] = 0
	while rounds<amount_of_rounds:
		next_states = {}
		#The amount of nodes in each state.R:8,I:4,E:2,S:1 (binary vector)
		for vert in g.Nodes():
			randChance=random.random()
			#S
			if states[vert.GetId()] == 1:
				#Chance to transition from S to E.
				if check_neighbors(vert,states) and randChance<=alpha:
					next_states[vert.GetId()]=2
					amounts['E']+=1
					amounts['S']-=1
					current_period[vert.GetId()]=0
					#Generate the incubation time threshold X sub e.
					current_threshold[vert.GetId()]=random.gauss(11,2)
					#incubation_days[random.randint(0,len(incubation_days)-1)]
				#Else remain in S.
				else:
					next_states[vert.GetId()]=1
			#E
			elif states[vert.GetId()]==2:
				#check the probability for transition to E.
				if current_threshold[vert.GetId()]> 0 and current_period[vert.GetId()] >= current_threshold[vert.GetId()]:
					current_period[vert.GetId()]=0
					next_states[vert.GetId()]=4
					#Generate the infection time threshold X sub i.
					current_threshold[vert.GetId()]=random.gauss(5,1)
					#infection_days[random.randint(0,len(infection_days)-1)]
					amounts['I']+=1
					amounts['E']-=1
					continue
				else:
					next_states[vert.GetId()]=2
				#increment tau sub e.
				current_period[vert.GetId()]+=1
			#I
			elif states[vert.GetId()]==4:
				#Chance of death/recovery occuring.
				if current_threshold[vert.GetId()]>0 and current_period[vert.GetId()] >= current_threshold[vert.GetId()]:
					next_states[vert.GetId()]=8
					amounts['R']+=1
					amounts['I']-=1
					continue
				else:
					next_states[vert.GetId()]=4
				#increment tau sub i.
				current_period[vert.GetId()]+=1
			#R remain in current state.
			elif states[vert.GetId()]==8:
				next_states[vert.GetId()]=8
		states=next_states
		rounds+=1
		#print rounds,"\tS:",amounts['S'],"  E:",amounts['E'],"  I:",amounts['I'],"  R:",amounts['R']
		#Break if every node is recovered/dead or cannot be infected
		if amounts['R']==g.GetNodes() or (amounts['R'] > 0 and amounts['E'] == 0 and amounts['I']==0):
			break
	return amounts