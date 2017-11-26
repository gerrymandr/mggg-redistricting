# PACKAGES
import pysal.network as nw
import matplotlib as plt
import numpy as np
import pysal as ps
import random as rdm
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection
import collections
import glob
import pandas as pd
import scipy

adj_lists_dir = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/adjacency_graphs_all/adj_lists"

adj_files = glob.glob(adj_lists_dir+'/*.csv')

save_dir = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/adjacency_graphs_all/adj_matrices/tracts"

for file in adj_files:
	state = file[-6:-4]
	# print(state)
	df = pd.read_csv(file)
	#print(df)
	adj_matrix = pd.crosstab(df[df.columns[0]],df[df.columns[1]])
	adj_matrix.to_csv(save_dir+"/csvs/"+state+"_tract_adjacency.csv",index=False,header=False)
	# scipy.io.savemat(save_dir+"/"+state+"_tract_adjacency.mat", mdict={"tracts_"+state:adj_matrix})
