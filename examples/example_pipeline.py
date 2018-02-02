from adjacency_graphs.algorithms.twostep import TwoStepGraph
#from adjacency_graphs.plots.mpl import visualize_adjacency_graph

shp_dir = 'tests/shapefiles/testershape.shp'
geoid_column = 'id'

my_graph = TwoStepGraph(shp_dir, geoid_column)

# Line below is broken
#fig = visualize_adjacency_graph(my_graph)
# fig.show()
