def drop_edge(mggg_graph, edge):
    """ Modify the neighbors attribute to remove one edge
        Inputs:
            mggg_graph (Graph): A graph object from adjacency_graphs.algorithms
            edge (tuple[integer, integer]): A tuple of vertices from which to
                                            remove an edge. (i, j) to remove
                                            the edge between i and j.
    """
    assert len(edge) == 2
    gph_edges = mggg_graph.neighbors

    assert edge[0] in gph_edges[edge[1]]
    assert edge[1] in gph_edges[edge[0]]

    gph_edges[edge[0]].remove(edge[1])
    gph_edges[edge[1]].remove(edge[0])
    mggg_graph.neighbors = gph_edges


def add_edge(mggg_graph, edge):
    """ Modify the neighbors attribute to add one edge
        Inputs:
            mggg_graph (Graph): A graph object from adjacency_graphs.algorithms
            edge (tuple[integer, integer]): A tuple of vertices from which to
                                            add an edge. (i, j) to add
                                            the edge between i and j.
    """
    assert len(edge) == 2
    gph_edges = mggg_graph.neighbors

    assert edge[0] not in gph_edges[edge[1]]
    assert edge[1] not in gph_edges[edge[0]]

    gph_edges[edge[0]].add(edge[1])
    gph_edges[edge[1]].add(edge[0])
    mggg_graph.neighbors = gph_edges
