from adjacency_graphs.MgggGraph import MgggGraph
from adjacency_graphs.plots.mpl import visualize_adjacency_graph

shp_dir = 'shapefiles/testershape.shp'
geoid_column = 'id'

my_graph = MgggGraph(shp_dir, geoid_column)
fig = visualize_adjacency_graph(my_graph)
fig.show()
