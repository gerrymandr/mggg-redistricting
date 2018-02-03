import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pysal.contrib.viz import mapping as maps


"""
visualize_adjacency_graph
create and visualize an adjacency graph of geometries in an shp file.

@param file_dir a string directory for the shp file which one wishes to analyze.
@param out_dir a string directory where one wishes to save the output image. Image
will not be saved if this is None.
"""
def visualize_adjacency_graph(file_dir, dbf_dir, id_column, out_dir=None):
	# open the file and obtain pysal geometries
	shp = ps.open(file_dir)
	# setting up matplot figure
	fig = plt.figure(figsize=(9,9))
	fig.set_facecolor('white')
	base = maps.map_poly_shp(shp)
	base.set_linewidth(0.75)
	base.set_facecolor('none')
	base.set_edgecolor('0.8')

	# Build a dictionary to associate geoid and index.
	data = ps.pdio.read_files(file_dir)
	gti = {} 
	for index, row in data.iterrows():
		gti[row[id_column]] = index
	# graph contains polygons matched to their neighbors, uses polygon identifiers
	graph = mggg_twostep(create_polymap(file_dir, dbf_dir, id_column))
	# obtain the centroids of polygons

	polygon_centroids = {x:y.centroid for x,y in enumerate(shp)}

	# connect centroids of the polygons using LineCollection
	edge_list = [(polygon_centroids[gti[poly1]], 
	              polygon_centroids[gti[poly2]]) for poly1,neighbors in graph.items() 
	             for poly2 in neighbors]


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
