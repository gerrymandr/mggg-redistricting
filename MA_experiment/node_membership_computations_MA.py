
# PACKAGES
# import pysal.network as nw
# import scipy
# import scipy.stats.stats
# from scipy.stats.stats import chisqprob
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
# import csv
import pandas as pd
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
	DISTRICT_TO_GEOID[district_polygon] = GEOID_LIST[i][0]

# print('done')
# print(STATE_TO_DISTRICTS)

"""

iterate over the tract files and compute the following
...

"""

# get entries in following format [(district GEOID), (tract_id [unsure how to get this effectively]), area of intersection]
# number of boundary tracts and number of member tracts
entries = []
node_membership = []
for tract_file in tract_files:
	shp = ps.open(tract_file)
	graph = twostep(shp)
	tid_to_poly = {x:y for x,y in enumerate(shp)}
	state = tract_file[-14:-12]
	# state_tracts = ps.cg.locators.PolygonLocator([poly for poly in shp]) # package bug ..
	for district in STATE_TO_DISTRICTS[state]:
		# tracts_to_consider = state_tracts.inside(district.bounding_box) # package bug ..
		# tracts_to_consider = graph.items()
		# ct = 0 #placeholder to tract IDs
		d = sg.asShape(district)
		dbox = sg.box(*sg.asShape(district).bounds)
		dboundary = set()
		dmember = set()

		for tid,tract in tid_to_poly.items():
			#print(tract)
			t = sg.box(*tract.bbox)
			if t.intersects(dbox):
				# print("yep1")
				if d.intersects(t):
					# print("yep2")
					area = d.intersection(t).area
					entries.append([DISTRICT_TO_GEOID[district], tid, area])
				# ct+=1
					if all(d.intersects(sg.asShape(tid_to_poly[x])) for x in graph[tid]):
						dmember.update([tid])
					else:
						dboundary.update([tid])
		node_membership.append([DISTRICT_TO_GEOID[district],len(dboundary),len(dmember)])



print(entries)
print(node_membership)
# print(tract_files[0])

# save results

df_entries = pd.DataFrame(entries)
df_node_membership = pd.DataFrame(node_membership)

df_entries.to_csv("district_to_tracts_overlap.csv", index=False, header = False)
df_node_membership.to_csv("node_membership.csv", index=False,header=False)

# with open("district_to_tracts_overlap.csv", "w") as f1:
# 	writer1 = csv.writer(f1)
# 	writer1.writerows(entries)

# with open("node_membership.csv", "w") as f2:
# 	writer2 = csv.writer(f2)
# 	writer2.writerows(node_membership)




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