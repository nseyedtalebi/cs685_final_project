import pickle

import matplotlib.pyplot as plt

with open('r0_er.pkl','r') as er:
	r0_er = pickle.load(er)
with open('r0_ba.pkl','r') as ba:
	r0_ba = pickle.load(ba)
with open('r0_ws_deg.pkl','r') as ws:
	r0_ws_deg = pickle.load(ws)
with open('r0_ws_beta.pkl','r') as ws:
	r0_ws_beta = pickle.load(ws)

def dict_results_to_lists(r0_values):
	keys = [key for key in sorted(r0_values.keys())]
	values = [r0_values[key] for key in keys]
	return keys,values

plt.plot(*dict_results_to_lists(r0_er))
plt.title('Estimated R0, ER graphs\n500 nodes, alpha=0.9, zeta=0.02')
plt.ylabel('R0')
plt.xlabel('Number of Edges')
plt.show()

plt.plot(*dict_results_to_lists(r0_ba))
plt.title('Estimated R0, BA graphs\n500 nodes, alpha=0.9, zeta=0.02')
plt.ylabel('R0')
plt.xlabel('Mean OutDegree')
plt.show()

plt.plot(*dict_results_to_lists(r0_ws_deg))
plt.title('Estimated R0, WS graphs (beta=0)\n500 nodes, alpha=0.9, zeta=0.02')
plt.ylabel('R0')
plt.xlabel('Mean OutDegree')
plt.show()

plt.plot(*dict_results_to_lists(r0_ws_beta))
plt.title('Estimated R_0, WS graphs (Degree=12)\n500 nodes, alpha=0.9, zeta=0.02')
plt.ylabel('R0')
plt.xlabel('Rewire Probability (% chance)')
plt.show()