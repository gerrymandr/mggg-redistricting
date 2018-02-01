import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pysal.contrib.viz import mapping as maps


def visualize_adjacency_graph(mggg_graph, fig=None, out_dir=None):
    """
    visualize_adjacency_graph
    create and visualize an adjacency graph of geometries in an shp file.

    @param file_dir a string directory for the shp file which one wishes to
            analyze.
    @param out_dir a string directory where one wishes to save the output
            image. Image will not be saved if this is None.
    """
    if not fig:
        fig = plt.figure(figsize=(9, 9))
    fig.set_facecolor('white')
    base = maps.map_poly_shp(mggg_graph.pysal_shp_obj)
    base.set_linewidth(0.75)
    base.set_facecolor('none')
    base.set_edgecolor('0.8')

    # obtain the centroids of polygons
    polygon_centroids = {x: y.centroid
                         for x, y in enumerate(mggg_graph.pysal_shp_obj)}

    # connect centroids of the polygons using LineCollection
    edge_list = ((polygon_centroids[poly1], polygon_centroids[poly2])
                 for poly1, neighbors in mggg_graph.neighbors.items()
                 for poly2 in neighbors)
    edge_list = LineCollection(edge_list)

    edge_list.set_linewidth(0.20)
    ax = maps.setup_ax([base, edge_list], [mggg_graph.pysal_shp_obj.bbox,
                                           mggg_graph.pysal_shp_obj.bbox])
    fig.add_axes(ax)
    return fig
