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
a graph using geographic identifiers if that is the key provided in the input.

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
get_district_member_and_boundary_entities
Output a list of lists [district_geoid, # of boundary nodes,
total # of member nodes]

sub-entities can be one of blocks, block groups, tracts

@param shp_and_dbf_file_dir a directory to shp and dbf files for sub-entities
@param cd_dbf_dir directory to a dbf file for the congressional districts
@param cd_shp_dir directory to an shp file for the congressional districts
@param sub_geoid_col string identifier for the geographic identifier field in the
sub-entity dbf file

"""
def get_district_member_and_boundary_entities(shp_and_dbf_file_dir, cd_dbf_dir, cd_shp_dir, sub_geoid_col):
	state_to_districts = get_state_to_districts_map(cd_dbf_dir,cd_shp_dir,state_col,cd_col)
	return [[cd,len(set(e for e,e_poly in create_polymap(shp,dbf,sub_geoid_col) if boundary_node(cd_poly,e_poly))),len(set(e for e,e_poly in create_polymap(shp,dbf,sub_geoid_col)))] for shp,dbf in get_dbf_shp_files(shp_and_dbf_file_dir) for cd,cd_poly in state_to_districts[shp[-14:-12]]]

"""
boundary_node
Determine if a polygon is a boundary node for another polygon

@param super super-unit polygon (ie. congressional district)
@param sub sub-unit polygon (ie. tract)

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
