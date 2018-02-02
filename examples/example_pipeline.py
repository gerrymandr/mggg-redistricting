from adjacency_graphs.algorithms import TwoStepGraph
from adjacency_graphs.plots.mpl import visualize_adjacency_graph
from matplotlib.pyplot import savefig

shp_dir = '../tests/shapefiles/testershape.shp'
geoid_column = 'id'

my_graph = TwoStepGraph(shp_dir, geoid_column)

# Line below is broken
fig = visualize_adjacency_graph(my_graph)
savefig('example.png')
