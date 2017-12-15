"""
This library contains several methods used in the computations for
district-to-tract overlap area as well as node membership computations (boundary
and member nodes)

author: Alejandro Velez
for use by the Metric Geometry and Gerrymandering Group and Gerrymandering analytics
enthusiasts
"""

"""
Packaged used are below. The library is built on top of pysal, pandas, shapely and
other libraries.
"""
import matplotlib as plt
import numpy as np
import pysal as ps
import random as rdm
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection
import glob
import collections
import shapely.geometry as sg
import pandas as pd

"""
create_polymap
Obtain a python dictionary mapping Census geographic entity GEOIDs (as defined in
https://www.census.gov/geo/reference/geoidentifiers.html) to pysal Polygon objects

@param shp_dir a string directory containing the shp file of interest
for the census geographic entity one wishes to explore

@param dbf_dir a string directory the dbf file of interest for the census
geographic entity one wishes to explore

@param geoid_column a string containing the identifier used to label the GEOID
column in the dbf file

@return a python dictionary mapping entity geographic identifiers to pysal polygons
"""
def create_polymap(shp_dir, dbf_dir, geoid_column):
	shp = ps.open(shp_dir)
	dbf = ps.open(dbf_dir)

	geoid_list = dbf.by_col_array(geoid_column)
	geom_list = [x for x in shp]
	return {geoid_list[i][0]:geom_list[i] for i in range(len(geom_list))}

"""
get_dbf_shp_files
Generate the shp and dbf files in a directory

@param directory string to the directory containing the shp and dbf files of
interest for the census geographic entities one wishes to explore

@yield shp,dbf file pairs
"""
def get_dbf_shp_files(directory):
	shp_files = glob.glob(directory+'/*.shp')
	dbf_files = glob.glob(directory+'/*.dbf')
	yield from zip(shp_files,dbf_files)

"""
mggg_twostep
Create an adjacency graph pairing census geographic entities to adjacencies. Outputs
a graph using geographic identifiers iff that is the key provided in the input.

Uses the High Performance Containers and Set Operations two-step algorithm
for node adjacency source:
http://conference.scipy.org/proceedings/scipy2014/pdfs/laura.pdf

@param polymap dictionary mapping the desired ID to their pysal geometries

@return adjacency graph as a python dictionary
"""
def mggg_twostep(polymap):
	shpFileObject = polymap

	numPoly = len(shpFileObject)

	vertices = collections.defaultdict(set)
	for i, s in shpFileObject.items():
		newvertices = s.vertices[:-1]
		for v in newvertices:
			vertices[v].add(i)

	w = collections.defaultdict(set)
	for neighbors in vertices.values():
		for neighbor in neighbors:
			w[neighbor] = w[neighbor] | neighbors
	return w

"""
visualize_adjacency_graph
create and visualize an adjacency graph of geometries in an shp file.

@param file_dir a string directory for the shp file which one wishes to analyze.
@param out_dir a string directory where one wishes to save the output image. Image
will not be saved if this is None.
"""
def visualize_adjacency_graph(file_dir, out_dir=None):
	# open the file and obtain pysal geometries
	shp = ps.open(file_dir)

	# setting up matplot figure
	fig = plt.figure(figsize=(9,9))
	fig.set_facecolor('white')
	base = maps.map_poly_shp(shp)
	base.set_linewidth(0.75)
	base.set_facecolor('none')
	base.set_edgecolor('0.8')

	# graph contains polygons matched to their neighbors, uses polygon identifiers
	graph = mggg_twostep(shp)

	# obtain the centroids of polygons
	polygon_centroids = {x:y.centroid for x,y in enumerate(shp)}

	# connect centroids of the polygons using LineCollection
	edge_list = [(polygon_centroids[poly1], polygon_centroids[poly2]) for poly1,neighbors in graph.items() for poly2 in neighbors]
	edge_list = LineCollection(edge_list)

	edge_list.set_linewidth(0.20)
	ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
	fig.add_axes(ax)

	# see your output
	show()

	# save your output
	if(out_dir is not None):
		savefig(out_dir)

	plt.close()


"""
get_state_to_districts_map
Create a python dictionary mapping state FIPS codes to a list of the
congressional districts belonging to the state.

@param dbf_dir directory to the census dbf file for the congressional districts
@param shp_dir directory to the census shp file for the congressional districts
@param state_col string identifier for the FIPS code field in the dbf file
@param cd_col string identifier for the geographic identifier field in the dbf
file

@return a python dictionary mapping state FIPS codes to a list of the
congressional districts belonging to the state represented as tuples of the
format (congressional geographic identifier, polygon object)
"""
def get_state_to_districts_map(dbf_dir, shp_dir, state_col, cd_col):
	district_list = [x for x in ps.open(shp_dir)]
	cd_dbf = ps.open(dbf_dir)
	state_list = cd_dbf.by_col_array(state_col)
	geoid_list = cd_dbf.by_col_array(cd_col)

	return {state[0]:[(geoid_list[i][0],district_list[i]) for i in range(len(district_list)) if state_list[i][0]==state[0]] for state in state_list}

"""

"""


"""
get_district_member_and_boundary_entities
Output a list of lists [district_geoid, # of boundary nodes,
total # of member nodes]
Output a list of lists [district_geoid, subentity_geoid, area of overlap, total area]

sub-entities can be one of blocks, block groups, tracts

@param shp_and_dbf_file_dir a directory to shp and dbf files for sub-entities
@param cd_dbf_dir directory to a dbf file for the congressional districts
@param cd_shp_dir directory to an shp file for the congressional districts
@param sub_geoid_col string identifier for the geographic identifier field in the
sub-entity dbf file
@param cd_col string identifier for the geographic identifier field in the dbf
file
@param begin starting index for the state identifier in sub-unit filenames
@param end ending index for the state identifier in the sub-unit filenames

"""
def get_district_member_and_boundary_entities(shp_and_dbf_file_dir, cd_dbf_dir, cd_shp_dir, sub_geoid_col, cd_col, begin, end):
	# zip tract shp filenames to corresponding dbf filenames
	files = get_dbf_shp_files(shp_and_dbf_file_dir)

	# map states to corresponding districts
	state_to_districts = get_state_to_districts_map(cd_dbf_dir,cd_shp_dir,state_col,cd_col)

	# initialize two lists for output
	entries = []
	node_membership = []

	# iterate over the sub-unit files
	for tract_file, dbf_file in files:
		# map identifiers to tract geometries
		GEOID_to_TRACT = create_polymap(tract_file,dbf_file,sub_geoid_col)

		# parse to obtain relevant state code
		state = tract_file[begin:end]
		
		# iterate over relevant districts to perform computations
		for geoID, district in state_to_districts[state]:
			# translate to shapely geometries 
			d = sg.asShape(district)
			dbox = sg.box(*sg.asShape(district).bounds)
			# initialize sets to count boundary and member nodes
			dboundary = set()
			dmember = set()
			# iterate over tracts 
			for tid,tract in GEOID_to_TRACT.items():
				# create bounding box for the district
				t = sg.box(*tract.bbox)
				# to save time, first check whether bounding boxes for tract and district intersect
				if t.intersects(dbox):
					tr = sg.asShape(tract)
					# check whether geometries actually intersect
					if d.intersects(tr):
						# compute area of overlap
						area = d.intersection(t).area
						# append to output
						entries.append([geoID, tid, area, area/t.area])

						# check whether node is boundary or member
						is_boundary = d.intersection(t.buffer(0.001)).area/t.buffer(0.001).area < 1
						if is_boundary:
							dboundary.update([tid])
						dmember.update([tid])
			# append an entry for this district
			node_membership.append([geoID,len(dboundary),len(dmember)])
	return node_membership, entries



	
	
"""
boundary_node
Determine if a polygon is a boundary node for another polygon

@param super super-unit polygon (ie. congressional district)
@param sub sub-unit polygon (ie. census tract)

return true iff sub is boundary node for super
"""
def boundary_node(supr, sub, b=0.0001, threshold=0):
	if !intersect(supr,sub):
		return False
	sg1=sg.asShape(supr)
	sg2=sg.box(*sub.bbox).buffer(b)
	if sg1.intersection(sg2).area/sg2.area<1-threshold:
		return True

	return False

def intersect(geom1, geom2):
	box1 = sg.box(*geom1.bbox)
	box2 = sg.box(*geom2.bbox)

	sg1 = sg.asShape(geom1)
	sg2 = sg.asShape(geom2)

	if box1.intersects(box2):
		if sg1.intersects(sg2):
			return True

	return False
