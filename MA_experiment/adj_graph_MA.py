"""
This file is meant to create an adjacency graph of US census blocks for
the state of Massachusetts. 

using data from
https://www.census.gov/geo/maps-data/data/cbf/cbf_tracts.html
"""

# PACKAGES
# import shapefile #experimenting with this library as well
import pysal.network as nw
import matplotlib as plt
import numpy as np
import pysal as ps
import random as rdm
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection

# INPUTS
# string for SHP file directory - user should adjust this as necessary
# using 2010 Census Data
file_dir = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/tract_file/tl_2010_78_tract10.shp"

# map out census blocks
shp = ps.open(file_dir)

# map all vertices to a centroid
# cents = {(round(v[0],9),round(v[1],9)): (round(s.centroid[0],9),round(s.centroid[1],9)) for s in shp for v in s.vertices}
cents = {v: s.centroid for s in shp for v in s.vertices}

# setting up matplot figure
fig = plt.figure(figsize=(9,9))
fig.set_facecolor('white')
base = maps.map_poly_shp(shp)
base.set_linewidth(0.75)
base.set_facecolor('none')
base.set_edgecolor('0.8')

# create a network to obtain the adjacency graph edges
MA_network = nw.network.Network(file_dir, unique_segs=True, node_sig=None)

# get an edge list and transform to a matplotlib collection
edge_list = []
for start, end in MA_network.edges:
	try:
		edge_list.append((cents[MA_network.node_coords[start]], cents[MA_network.node_coords[end]]))
	except:
		# TODO: here's the line which could be responsible for the missing edges - unsure how to handle
		# some coordinates don't appear in the map, this is likely due to small computational discrepancies 
		# at the lower digits of the float --> rounding could help but also takes away edges due to inaccuracies
		continue 

edge_list = LineCollection(edge_list)

#maps._add_axes2col(edge_list,shp.bbox) #figuring out if this could be useful
edge_list.set_linewidth(0.20)
ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
fig.add_axes(ax)
show()

# use this line to save your output
# savefig("Massachusetts_adjacency_graph.png")



