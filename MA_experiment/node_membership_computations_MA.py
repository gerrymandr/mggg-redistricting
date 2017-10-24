
# PACKAGES
import pysal.network as nw
import matplotlib as plt
import numpy as np
import pysal as ps
import random as rdm
from pysal.contrib.viz import mapping as maps
from pylab import *
from matplotlib.collections import LineCollection
import glob
import collections
import shapely.geometry
# import shapefile

# INPUTS
# directory where tract files are contained
tract_directory = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/tract_file"
# 2013 congressional districts file
cdistricts_file = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/cb_2013_us_cd113_500k/cb_2013_us_cd113_500k.shp"

# create list of path names to the tract files
tract_files = glob.glob(tract_directory+'/*.shp')

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
#####################################################

# obtain a list for the states for each congressional district
cdistricts_dbf = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/MA_experiment/MA_case/cb_2013_us_cd113_500k/cb_2013_us_cd113_500k.dbf"
cd_dbf = ps.open(cdistricts_dbf)
STATE_LIST = cd_dbf.by_col_array('STATEFP')
DISTRICT_LIST = [x for x in ps.open(cdistricts_file)]
GEOID_LIST = cd_dbf.by_col_array('GEOID')
# print(dbf.by_col_array('STATEFP'))

# create a dictionaries 
# for each state, map to a list of its districts (as PySAL Polygon objects)
# for each district, map to its GEOID
STATE_TO_DISTRICTS = {}
DISTRICT_TO_GEOID = {}
for i in range(len(DISTRICT_LIST)):
	state = STATE_LIST[i][0]
	district_polygon = DISTRICT_LIST[i]
	if state not in STATE_TO_DISTRICTS:
		STATE_TO_DISTRICTS[state]=[]
	STATE_TO_DISTRICTS[state].append(district_polygon)
	DISTRICT_TO_GEOID[district_polygon] = GEOID_LIST[i]

# print('done')
# print(STATE_TO_DISTRICTS)

"""

iterate over the tract files and compute the following
For each district, compute:
number of boundary tracts (at least one neighbor inside the district and at least one neighbor out)
number of member tracts (>= 10% of the tract in the district)

"""

# print(shapely.geometry.asShape(STATE_TO_DISTRICTS['04'][0]).intersection(shapely.geometry.asShape(STATE_TO_DISTRICTS['04'][1])).area)


# print([x for x in ps.open(cdistricts_file)]) # --> generator for Polygon objects


# sf = shapefile.Reader(cdistricts_file)
# # print(sf.fields)
# # GEOID_index = sf.fields.index(['GEOID', 'C', 4, 0])
# shapeRecords = sf.shapeRecords()

# print([x.record[GEOID_index-1] for x in shapeRecords]) #Use GEOID for pairing state ids to congressional

### MAY NOT NEED THIS!!
# # create a graph which includes all tracts 
# tract_graph = {}
# for shp_file in tract_files:
# 	shp = ps.open(shp_file)
# 	tract_graph.update(twostep(shp))
# ### WARNING: ^ this takes a few seconds..




# # test two-step on one of the files
# shp = ps.open(tract_files[0])
# print(twostep(shp))


# #TESTS
# print(tract_files)