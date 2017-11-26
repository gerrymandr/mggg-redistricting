
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
tract_directory = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/adjacency_graphs_all/MA_case/tract_file"
# 2013 congressional districts file
cdistricts_file = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/adjacency_graphs_all/MA_case/cb_2013_us_cd113_500k/cb_2013_us_cd113_500k.shp"
threshold = 0.00001 # for determining boundary nodes

# create list of path names to the tract files
tract_files = glob.glob(tract_directory+'/*.shp')
dbf_files = glob.glob(tract_directory+'/*.dbf')
files = zip(tract_files,dbf_files)

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

def modified_twostep(d):
	shpFileObject = d
	# if shpFileObject.type != ps.cg.Polygon:
	# 	return
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
#####################################################

# obtain a list for the states for each congressional district
cdistricts_dbf = "/Users/avelez/Documents/MGGG_UROP/state-adjacency-graphs/adjacency_graphs_all/MA_case/cb_2013_us_cd113_500k/cb_2013_us_cd113_500k.dbf"
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
for tract_file, dbf_file in files:
	shp = ps.open(tract_file)
	# tid_to_poly = {x:y for x,y in enumerate(shp)}
	state = tract_file[-14:-12]

	dbf = ps.open(dbf_file)
	# print(dbf.header)
	GEOID_LIST = dbf.by_col_array('GEOID10')
	tract_list = [x for x in shp]
	GEOID_to_TRACT = {GEOID_LIST[i][0]:tract_list[i] for i in range(len(tract_list))}

	# graph = modified_twostep(GEOID_to_TRACT)

	
	for district in STATE_TO_DISTRICTS[state]:
		d = sg.asShape(district)
		dbox = sg.box(*sg.asShape(district).bounds)
		dboundary = set()
		dmember = set()
		chainD = ps.cg.shapes.Chain(district.vertices)

		for tid,tract in GEOID_to_TRACT.items():
			t = sg.box(*tract.bbox)
			chainT = ps.cg.shapes.Chain(tract.vertices)
			if t.intersects(dbox):
				tr = sg.asShape(tract)
				if d.intersects(tr):
					# area = d.intersection(t).area
					# entries.append([DISTRICT_TO_GEOID[district], tid, area, area/t.area])

					# check if boundaries intersect
					#they_do = any(sg.asShape(dc).intersects(sg.asShape(tc)) for dc in chainD.segments for tc in chainT.segments)
					they_do = d.intersection(t.buffer(0.001)).area/t.buffer(0.001).area < 1
					if they_do:
						dboundary.update([tid])
					dmember.update([tid])

					# determine whether the tract is boundary or area
					# if area/t.area < (1.0-threshold):
					# 	dboundary.update([tid])
					#elif check if touch boundary --> boundary
					#else its an area node
					
					# if area/t.area >= (1.0-threshold):
					# 	dmember.update([tid])
					# else:
					# 	dboundary.update([tid])
		node_membership.append([DISTRICT_TO_GEOID[district],len(dboundary),len(dmember)])



# print(entries)
# print(node_membership)
# print(tract_files[0])

# save results

# df_entries = pd.DataFrame(entries)
df_node_membership = pd.DataFrame(node_membership)

#df_entries.to_csv("district_to_tracts_overlap_new.csv", index=False, header = False)
df_node_membership.to_csv("node_membership_new.csv", index=False,header=False)

