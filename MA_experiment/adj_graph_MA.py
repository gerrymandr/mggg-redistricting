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
import collections

# INPUTS
# string for SHP file directory - user should adjust this as necessary
# using 2010 Census Data
file_dir = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/tract_file/tl_2010_25_tract10.shp"

# define the High Performance Containers and Set Operations two-step algorithm for node adjacency
# source: http://conference.scipy.org/proceedings/scipy2014/pdfs/laura.pdf
def twostep(fname):
	shpFileObject = fname
	if shpFileObject.type != ps.cg.Polygon:
		return
	numPoly = len(shpFileObject)

	vertices = collections.defaultdict(set)
	for i, s in enumerate(shpFileObject):
		newvertices = s.vertices[:-1]
		for v in newvertices:
			vertices[v].add(i)

	w = collections.defaultdict(set)
	for neighbors in vertices.values():
		for neighbor in neighbors:
			w[neighbor] = w[neighbor] | neighbors
	return w

# map out census blocks
shp = ps.open(file_dir)

# setting up matplot figure
fig = plt.figure(figsize=(9,9))
fig.set_facecolor('white')
base = maps.map_poly_shp(shp)
base.set_linewidth(0.75)
base.set_facecolor('none')
base.set_edgecolor('0.8')

# graph contains polygons matched to their neighbors, uses polygon identifiers
graph = twostep(shp)

# obtain the centroids of polygons
polygon_centroids = {x:y.centroid for x,y in enumerate(shp)}

# obtain an edge_list
edge_list = [(polygon_centroids[poly1], polygon_centroids[poly2]) for poly1,neighbors in graph.items() for poly2 in neighbors]
edge_list = LineCollection(edge_list)

#maps._add_axes2col(edge_list,shp.bbox) #figuring out if this could be useful
edge_list.set_linewidth(0.20)
ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
fig.add_axes(ax)

# use this line to see your output
# show()

# use this line to save your output
# savefig("Massachusetts_adjacency_graph.png")



