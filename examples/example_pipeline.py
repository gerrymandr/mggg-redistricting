from adjacency_graphs.algorithms import TwoStepGraph
from adjacency_graphs.plots.mpl import visualize_adjacency_graph
from matplotlib.pyplot import savefig

# Here we set the shape directory and the column to use for vertices
shp_dir = '../tests/shapefiles/testershape.shp'
id_column = 'id'

# Now, run the twostep algorithm as found in algorithms.
# This will export a MgggGraph object.
my_graph = TwoStepGraph(shp_dir, id_column)

# We can plot graphs using functions in `plots`
fig = visualize_adjacency_graph(my_graph)
savefig('example.png')

# Graphs have a number of associated methods. Here
# we export our dataframe of vertices and edges to csv.
my_graph.export_graph('example_graph.csv')
