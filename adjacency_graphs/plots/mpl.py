import matplotlib.pyplot as plt
import pysal as ps
from matplotlib.collections import LineCollection
from pysal.contrib.viz import mapping as maps


def visualize_adjacency_graph(mggg_graph, out_dir=None):
    ''' Visualize an adjacency graph
        Input: 
            mggg_graph (Graph): A graph object from adjacency_graphs.algorithms
            out_dir (string, optional): Path to the output file. If none provided,
                                        no file will be created
        Output:
            fig (matplotlib.pyplot): An object which can be plotted
    '''
    # open the file and obtain pysal geometries
    shp = mggg_graph.loaded_geodata
    # setting up matplot figure
    fig = plt.figure(figsize=(9, 9))
    fig.set_facecolor('white')
    base = maps.map_poly_shp(shp)
    base.set_linewidth(0.75)
    base.set_facecolor('none')
    base.set_edgecolor('0.8')

    # Build a dictionary to associate geoid and index.
    data = mggg_graph.shape_df
    gti = {}
    for index, row in data.iterrows():
        gti[row[mggg_graph.id_column]] = index
    # graph contains polygons matched to their neighbors, uses polygon identifiers
    graph = mggg_graph.neighbors
    # obtain the centroids of polygons

    polygon_centroids = {x: y.centroid for x, y in enumerate(shp)}

    # connect centroids of the polygons using LineCollection
    edge_list = [(polygon_centroids[gti[poly1]],
                  polygon_centroids[gti[poly2]]) for poly1, neighbors in graph.items()
                 for poly2 in neighbors]

    edge_list = LineCollection(edge_list)
    edge_list.set_linewidth(0.20)
    ax = maps.setup_ax([base, edge_list], [shp.bbox, shp.bbox])
    fig.add_axes(ax)

    # save your output
    if(out_dir is not None):
        savefig(out_dir)
    return fig
