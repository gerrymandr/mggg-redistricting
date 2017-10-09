"""
This file is meant to create an adjacency graph of US census blocks for
the state of Massachusetts. 

using data from
https://www.census.gov/geo/maps-data/data/cbf/cbf_tracts.html
"""

# PACKAGES
import shapefile
import pysal.network as nw

# INPUTS
# string for SHP file directory
file_dir = "/Users/avelez/Documents/MGGG_UROP/adjacency_graph/MA_case/cb_2016_25_tract_500k/cb_2016_25_tract_500k.shp"

# # Read Shapefile
# shp_file_reader = shapefile.Reader(file_dir)

# # get list of shapefile's geometry
# file_geometry = shp_file_reader.shapes()

# #TESTS
# print("boundary box for first element of the geometry is: ", file_geometry[0].bbox)
# print("fields are: ", shp_file_reader.fields)
# print("records are: ", [rec for rec in shp_file_reader.records()])

MA_network = nw.network.Network(file_dir, unique_segs=True)

# #TESTS for the network
# print("adjacency list for our network is: \n", MA_network.adjacencylist)
# print([x for x in MA_network.adjacencylist])

# transform to coordinates-based graph
coordinates_to_ids = {v:k for k,v in MA_network.nodes.items()}

network_dict = {coordinates_to_ids[v]:[coordinates_to_ids[x] for x in MA_network.adjacencylist[v]] for v in MA_network.adjacencylist}

# #TEST
# print("adjacency graph for our network is: ", network_dict)



