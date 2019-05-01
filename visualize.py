import sys
import matplotlib.pyplot as plt
import numpy as np

#Read in the file output by the simulation and graph it.
if len(sys.argv)!=4:
	print("Improper usage, call as",sys.argv[0]," file_to_visualize variations numOfEach\n")
	sys.exit(1)

states={0:{},1:{},2:{},3:{}}
labels=['S','E','I','R']
sizes=[]
baseStates=[]
Nodes=0
Edges=0
current_line=0
basename=sys.argv[1]
maxVars=int(sys.argv[2])
numEach=int(sys.argv[3])

index=0
variations=0
while variations<maxVars:
	index=0
	while index<numEach:
		size=[0]
		name=''
		if variations==0:
			name=basename+str(index)+'.txt'
		else:
			name=str(variations+1)+basename+str(index)+'.txt'
		print(name)
		with open(name,'r') as fp:
			line=fp.readline()
			splt=line.split(',')
			Nodes=int(splt[0])
			Edges=int(splt[1])
			line=fp.readline()
			current_line=0
			while line:
				items=line.split(',')
				if current_line not in states[0]:
					states[0][current_line]=[]
					states[1][current_line]=[]
					states[2][current_line]=[]
					states[3][current_line]=[]
				states[0][current_line].append(int(items[0]))
				states[1][current_line].append(int(items[1]))
				states[2][current_line].append(int(items[2]))
				states[3][current_line].append(int(items[3]))
				if size[len(size)-1]<current_line:
					size.append(current_line)
					
				current_line+=1
				line=fp.readline()
		if len(size)>len(sizes):
			sizes=size
		baseStates.append(states)
		index+=1
	variations+=1

avg_states={0:[],1:[],2:[],3:[]}
print(states)
for comparts in states:
	for timesteps in states[comparts]:
		total=0
		for value in states[comparts][timesteps]:
			total+=value
		avg_states[comparts].append(total/len(states[comparts][timesteps]))

#print(avg_states)
print(avg_states[1][4])
state_nums=4
colors = [plt.cm.Spectral(each)
			  for each in np.linspace(0, 1,state_nums)]

index=0
for i in range(0,len(states)):
	plt.plot(sizes,avg_states[i],markerfacecolor=colors[index],markeredgecolor='k',markersize=5,label=labels[index])
	index+=1

header=''
if sys.argv[1][0:2]=='ER':
	header='ER Graph (Nodes: '+str(Nodes)+', Edges:'+str(Edges)+')'
elif sys.argv[1][0:2]=='WS':
	header='WS Graph (Nodes: '+str(Nodes)+', Edges:'+str(Edges)+')'
elif sys.argv[1][0:2]=='BA':
	header='BA Graph (Nodes: '+str(Nodes)+', Edges:'+str(Edges)+')'

plt.title(header)
plt.ylabel('number in state')
plt.xlabel('time')
plt.legend()
plt.show()
			  