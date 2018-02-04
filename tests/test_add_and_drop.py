from adjacency_graphs.utils.edge_modification import add_edge, drop_edge


class MyGraph(object):
    def __init__(self):
        dict = {0: set([0, 1]), 1: set([0, 1]), 2: set([2])}
        self.neighbors = dict


def test_add_edge():
    graph = MyGraph()
    add_edge(graph, (1, 2))
    assert 2 in graph.neighbors[1]
    assert 1 in graph.neighbors[2]


def test_drop_edge():
    graph = MyGraph()
    drop_edge(graph, (0, 1))
    assert 0 not in graph.neighbors[1]
    assert 1 not in graph.neighbors[0]
