#Written by Nima
import pickle

import matplotlib.pyplot as plt
from seir_nima import dict_results_to_lists

with open('mses.pkl','r') as inf:
    mses = pickle.load(inf)
for method,values in mses.items():
    plt.plot(*dict_results_to_lists(values))
    plt.title('MSE for Different Values of i for '+method)
    plt.show()