#Written by Nima
import pickle

import matplotlib.pyplot as plt
from seir_nima import dict_results_to_lists

with open('mses.pkl','r') as inf:
    mses = pickle.load(inf)
for method,values in mses.items():
    plt.plot(*dict_results_to_lists(values))
    if method == 'er':
    	plt.title('MSE for Different Number of Edges')
    	plt.xlabel('# edges/# nodes')
    else:
    	plt.title('MSE for Different OutDegrees for '+method)
    	plt.xlabel('OutDegree')
    plt.ylabel('MSE')
    plt.show()