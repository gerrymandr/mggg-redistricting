from adjacency_graphs.algorithms import TwoStepGraph
from adjacency_graphs.plots.mpl import visualize_adjacency_graph
from matplotlib.pyplot import savefig
from adjacency_graphs.utils.export_graph import export_graph

shp_dir = '../tests/shapefiles/testershape.shp'
geoid_column = 'id'

my_graph = TwoStepGraph(shp_dir, geoid_column)

# Line below is broken
fig = visualize_adjacency_graph(my_graph)
savefig('example.png')

export_graph(my_graph, 'example_graph.csv')
