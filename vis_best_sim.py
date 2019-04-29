import pickle
from collections import defaultdict

import matplotlib.pyplot as plt
from seir import dict_results_to_lists
from simulations import load_dublin_case_data

def get_by_week(sim_results):
    by_week = defaultdict(lambda x:0.0)
    for day in sim_results:
        if day % 7 == 0 and day > 0:
            by_week[(day/7)] = sim_results[day]
    return by_week

dublin = load_dublin_case_data()
#10000 runs
labels=['S','E','I','R']
with open('best_fit.pkl','r') as inf:
    runs = pickle.load(inf)
by_week = get_by_week(runs)
timesteps,seir_counts = dict_results_to_lists(by_week)
for i in range(0,4):
    plt.plot(timesteps,[step[i] for step in seir_counts],label=labels[i],marker='.')
plt.plot(*dict_results_to_lists(dublin),label='Dublin I',marker='.')
plt.title('Dublin Outbreak Simulation\nAverage of 10000 runs')
plt.xlabel('Weeks')
plt.ylabel('People')
plt.legend()
plt.show()