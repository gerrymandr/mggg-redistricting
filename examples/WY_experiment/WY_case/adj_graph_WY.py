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
import networkx as nx
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection


def distance(p0, p1):
    """
    :param p0: first point
    :param p1: second point
    :return: distance between first point and second point
    """
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def share_vertex(the_first_shape, the_second_shape, shape_vertices_dict):
    """"
    :param the_first_shape: a shape
    :param the_second_shape: another shape
    :param shape_vertices_dict: dictionary that maps shape to all of the vertices of that shape
    :return: True if shapes share at least one vertex, False otherwise
    """
    for the_first_vertex in shape_vertices_dict[the_first_shape]:
        for the_second_vertex in shape_vertices_dict[the_second_shape]:
            if distance(the_first_vertex, the_second_vertex) < 1 / (10 ** 10):
                return True
    return False


# INPUTS
# string for SHP file directory - user should adjust this as necessary
file_dir = '/Users/Sarah/Documents/School Docs 17-18/MGGG UROP/Adjacency/state-adjacency-graphs/WY_experiment/WY_case/cb_2016_56_tract_500k/cb_2016_56_tract_500k.shp'

# map out census blocks
shp = ps.open(file_dir)

# empty graph to get adjacency
G = nx.Graph()

# map all vertices to a shape
vertex_collections = {}
for s in shp:
    vertex_collections[s] = []
    G.add_node(s)
    for v in s.vertices:
        vertex_collections[s].append(v)

# collect lines between centroids of adjacent shapes
edge_list = []
for first_shape in vertex_collections.keys():
    for second_shape in vertex_collections.keys():
        if first_shape == second_shape:
            continue
        if share_vertex(first_shape, second_shape, vertex_collections):
            edge_list.append((first_shape.centroid, second_shape.centroid))
            G.add_edge(first_shape, second_shape)

edge_list = LineCollection(edge_list)

# setting up matplot figure
fig = plt.figure(figsize=(9, 9))
fig.set_facecolor('white')
base = maps.map_poly_shp(shp)
base.set_linewidth(0.75)
base.set_facecolor('none')
base.set_edgecolor('0.8')
edge_list.set_linewidth(0.20)
ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
fig.add_axes(ax)
show()

# use this line to save your output
# savefig("Wyoming_adjacency_graph.png")
