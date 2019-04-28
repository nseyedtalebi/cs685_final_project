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
plt.show()

plt.plot(*dict_results_to_lists(r0_ba))
plt.show()

plt.plot(*dict_results_to_lists(r0_ws_deg))
plt.show()

plt.plot(*dict_results_to_lists(r0_ws_beta))
plt.show()