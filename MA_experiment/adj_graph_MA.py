"""
This file is meant to create an adjacency graph of US census blocks for
the state of Massachusetts. 

using data from
https://www.census.gov/geo/maps-data/data/cbf/cbf_tracts.html
"""

# PACKAGES
# import shapefile
import pysal.network as nw
# %matplotlib inline
import matplotlib as plt
import numpy as np
import pysal as ps
import random as rdm
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection

# INPUTS
# string for SHP file directory - user should adjust this as necessary
file_dir = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/cb_2016_25_tract_500k/cb_2016_25_tract_500k.shp"

# map out census blocks
shp = ps.open(file_dir)
# poly = shp[0]
# print(poly.points)

# map all vertices to a centroid
# cents = {(round(v[0],9),round(v[1],9)): (round(s.centroid[0],9),round(s.centroid[1],9)) for s in shp for v in s.vertices}
# cents = {s.centroid: v for s in shp for v in s.vertices}
cents = {v: s.centroid for s in shp for v in s.vertices}

fig = plt.figure(figsize=(9,9))
fig.set_facecolor('white')
base = maps.map_poly_shp(shp)
base.set_linewidth(0.75)
base.set_facecolor('none')
base.set_edgecolor('0.8')
# ax = maps.setup_ax([base],[shp.bbox])
# fig.add_axes(ax)
# show()

# create a network to obtain the adjacency graph edges
MA_network = nw.network.Network(file_dir, unique_segs=True, node_sig=None)
# MA_network.extractgraph()

# map block ids to coordinates
# coordinates_to_ids = {v:k for k,v in MA_network.nodes.items()}

# get an edge list and transform to a matplotlib collection
# edge_list = [[coordinates_to_ids[u], coordinates_to_ids[v]] for u in MA_network.adjacencylist for v in MA_network.adjacencylist[u]]
# edge_list = set([(cents[MA_network.node_coords[e[0]]], cents[MA_network.node_coords[e[1]]]) for e in MA_network.edges])
edge_list = []
for start, end in MA_network.edges:
	try:
		edge_list.append((cents[MA_network.node_coords[start]], cents[MA_network.node_coords[end]]))
	except:
		continue
# print(edge_list)
edge_list = LineCollection(edge_list)

#maps._add_axes2col(edge_list,shp.bbox)
edge_list.set_linewidth(0.20)
ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
fig.add_axes(ax)
show()

# savefig("Massachusetts_adjacency_graph.png")


# # Read Shapefile
# shp_file_reader = shapefile.Reader(file_dir)

# # get list of shapefile's geometry
# file_geometry = shp_file_reader.shapes()

# # #TESTS
# # print("boundary box for first element of the geometry is: ", file_geometry[0].bbox)
# # print("fields are: ", shp_file_reader.fields)
# # print("records are: ", [rec for rec in shp_file_reader.records()])

# MA_network = nw.network.Network(file_dir, unique_segs=True)

# # #TESTS for the network
# # print("adjacency list for our network is: \n", MA_network.adjacencylist)
# # print([x for x in MA_network.adjacencylist])

# # transform to coordinates-based graph
# coordinates_to_ids = {v:k for k,v in MA_network.nodes.items()}

# network_dict = {coordinates_to_ids[v]:[coordinates_to_ids[x] for x in MA_network.adjacencylist[v]] for v in MA_network.adjacencylist}

# #TEST
# print("adjacency graph for our network is: ", network_dict)

# plot the shp map

