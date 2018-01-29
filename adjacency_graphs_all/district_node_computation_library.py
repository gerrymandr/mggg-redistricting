"""
This library contains several methods used in the computations for
district-to-subunit overlap area as well as subunit membership computations 
(boundary and member subunits)

author: Alejandro Velez
for use by the Metric Geometry and Gerrymandering Group and Gerrymandering analytics
enthusiasts
"""

"""
Packages used are below. The library is built on top of pysal, pandas, shapely and
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
import threading
from shapely.geometry import mapping
import fiona

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
Thread class definitions - these are used to perform parallel overlap and 
membership computations 
"""
class file_thread(threading.Thread):
	def __init__(self,subunit_file,dbf_file,geoid_col,state_to_districts_map,overlap_list,membership_list,begin,end, threshold, boundary_buffer,writer):
		threading.Thread.__init__(self)
		self.subunit_file = subunit_file
		self.dbf_file = dbf_file
		self.geoid_col = geoid_col
		self.state_to_districts = state_to_districts_map
		self.entries = overlap_list
		self.node_membership = membership_list
		self.begin = begin
		self.end = end
		self.threshold = threshold
		self.boundary_buffer = boundary_buffer
		self.w = writer

	def run(self):
		# map identifiers to subunit geometries
		geoID_to_subunit = create_polymap(self.subunit_file,self.dbf_file,self.geoid_col)

		# parse to obtain relevant state code
		state = self.subunit_file[self.begin:self.end]

		threads = []

		for geoID, district in self.state_to_districts[state]:
			thread = unit_thread(geoID_to_subunit, self.entries,self.node_membership,geoID,district,self.threshold, self.boundary_buffer, self.w)
			thread.start()
			threads.append(thread)
		for t in threads:
			t.join()

class unit_thread(threading.Thread):
	def __init__(self,subunit_map, overlap_list, membership_list,geoID,unit,threshold,boundary_buffer, writer):
		threading.Thread.__init__(self)
		self.geoID_to_subunit = subunit_map
		self.entries = overlap_list
		self.node_membership = membership_list
		self.geoID = geoID
		self.unit = unit
		self.threshold = threshold
		self.boundary_buffer = boundary_buffer
		self.w = writer

	def run(self):
		# create shapely geometries
		d = sg.asShape(self.unit)
		dbox = sg.box(*d.bounds)
		# initialize sets to count boundary and member nodes
		dboundary = set()
		dmember = set()
		setLock = threading.Lock()
		listLock = threading.Lock()
		threads = []
		# iterate over subunits
		for sid,subunit in self.geoID_to_subunit.items():
			thr = subunit_thread(sid,subunit,self.entries,self.node_membership,self.geoID,d,dbox,setLock,listLock,self.threshold,self.boundary_buffer,dboundary,dmember, self.w)
			thr.start()
			threads.append(thr)
		# Wait for all threads to terminate
		for t in threads:
			t.join()
		# update membership list
		self.node_membership.append([self.geoID,len(dboundary),len(dmember)])

class subunit_thread(threading.Thread):
	def __init__(self,subunit_id,subunit_geom,entries,node_membership,unit_geoID,unit,unit_bbox,setLock,listLock,threshold,boundary_buffer,dboundary,dmember,writer):
		threading.Thread.__init__(self)
		self.sid = subunit_id
		self.subunit = subunit_geom
		self.entries = entries
		self.node_membership = node_membership
		self.unit_geoID = unit_geoID
		self.unit = unit
		self.unit_bbox = unit_bbox
		self.setLock = setLock
		self.listLock = listLock
		self.threshold = threshold
		self.boundary_buffer = boundary_buffer
		self.dboundary = dboundary
		self.dmember = dmember
		self.w = writer

	def run(self):
		# create bounding box for the subunit
		s = sg.box(*self.subunit.bbox)
		# to save time, first check whether bounding boxes for unit and
		# subunit intersect
		if s.intersects(self.unit_bbox):
			s_shapely = sg.asShape(self.subunit)
			# check whether geometries actually intersect
			if self.unit.intersects(s_shapely):
				# compute area of intersection
				try:
					area = self.unit.intersection(s_shapely).area
					s_area = s_shapely.area
				except: # handle cases where subunit shape is not well-defined
					area = self.unit.intersection(s).area
					s_area = s.area

				overlap_percentage = area/s_area

				# check if overlap threshold is met
				if overlap_percentage<self.threshold:
					return

				# append to overlap list
				with self.listLock:
					self.entries.append([self.unit_geoID,self.sid,area,overlap_percentage])

				# check if subunit is boundary or member
				is_boundary = self.unit.intersection(s_shapely.buffer(s_area)).area/s_shapely.buffer(s_area).area<1
				with self.setLock: # acquire setLock
					if is_boundary:
						self.dboundary.update([self.sid])
					self.dmember.update([self.sid])
					self.w.write({
						'geometry':mapping(self.subunit),
						'properties':{'is boundary':int(is_boundary), 'id':str(self.sid)},
						})








"""
get_district_member_and_boundary_entities
Output a list of lists [district_geoid, # of boundary nodes,
total # of member nodes]
Output a list of lists [district_geoid, subentity_geoid, area of overlap, percentage_overlap]

sub-entities can be one of blocks, block groups, tracts

@param shp_and_dbf_file_dir a directory to shp and dbf files for sub-entities
@param cd_dbf_dir directory to a dbf file for the congressional districts
@param cd_shp_dir directory to an shp file for the congressional districts
@param sub_geoid_col string identifier for the geographic identifier field in the
sub-entity dbf file
@param cd_col string identifier for the geographic identifier field in the dbf
file
@param state_col string identifier for the FIPS code field in the district dbf file
@param begin starting index for the state identifier in sub-unit filenames
@param end ending index for the state identifier in the sub-unit filenames
@param name of the shp file to be output for visualization of boundary and member nodes
@param threshold for node membership, default is 0.1 (10%)
@param boundary_buffer to be added to subunit boundaries for computation accurary, default is 0.001

"""
def get_district_member_and_boundary_entities(shp_and_dbf_file_dir, cd_dbf_dir, cd_shp_dir, sub_geoid_col, cd_col, state_col, begin, end, name, threshold=0.1, boundary_buffer=0.001):
	# zip tract shp filenames to corresponding dbf filenames
	files = get_dbf_shp_files(shp_and_dbf_file_dir)

	# map states to corresponding districts
	state_to_districts = get_state_to_districts_map(cd_dbf_dir,cd_shp_dir,state_col,cd_col)

	# initialize two lists for output
	entries = []
	node_membership = []
	threads = []

	# initialize an shp file to write objects to for visualization purposes

	# schema for the file
	schema = {
	'geometry':'Polygon',
	'properties':{'is boundary':'int','id':'str'}
	}

	with fiona.open(name,'w','ESRI Shapefile', schema) as output:

		# iterate over the sub-unit files, multi-thread
		for subunit_file, dbf_file in files:
			thread = file_thread(subunit_file,dbf_file,sub_geoid_col,state_to_districts,entries,node_membership,begin,end,threshold,boundary_buffer,output)
			thread.start()
			threads.append(thread)

		#check all threads terminated
		for t in threads:
			t.join()

	return entries,node_membership
