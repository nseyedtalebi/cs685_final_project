import sys
import matplotlib.pyplot as plt
import numpy as np

#Read in the file output by the simulation and graph it.
if len(sys.argv)!=2:
	print("Improper usage, call as",sys.argv[0]," file_to_visualize\n")
	sys.exit(1)

states={0:[],1:[],2:[],3:[]}
labels=['S','E','I','R']
size=[]
Nodes=0
Edges=0
current_line=0
with open(sys.argv[1],'r') as fp:
	line=fp.readline()
	while line:
		items=line.split(',')
		states[0].append(float(items[0]))
		states[1].append(float(items[1]))
		states[2].append(float(items[2]))
		states[3].append(float(items[3]))
		size.append(current_line)
		current_line+=1
		line=fp.readline()

state_nums=4
colors = [plt.cm.Spectral(each)
			  for each in np.linspace(0, 1,state_nums)]

index=0
for i in range(0,len(states)):
	plt.plot(size,states[i],markerfacecolor=colors[index],markeredgecolor='k',markersize=5,label=labels[index])
	index+=1

plt.ylabel('number in state')
plt.xlabel('time')
plt.legend()
plt.show()

			  