import os
from adjacency_graphs.algorithms import TwoStepGraph

thisdir = os.path.dirname(__file__)
shp_dir = os.path.join(os.path.dirname(thisdir), 'tests', 'shapefiles')


def test_add_edge():
    graph = TwoStepGraph(os.path.join(shp_dir, 'testershape.shp'),
                         id_column='id')
    graph.add_edge((1, 3))
    assert 1 in graph.neighbors[3]
    assert 3 in graph.neighbors[1]


def test_drop_edge():
    graph = TwoStepGraph(os.path.join(shp_dir, 'testershape.shp'),
                         id_column='id')
    graph.drop_edge((0, 1))
    assert 0 not in graph.neighbors[1]
    assert 1 not in graph.neighbors[0]
