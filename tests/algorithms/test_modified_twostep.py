import os

from adjacency_graphs.algorithms import ModifiedTwoStepGraph

thisdir = os.path.dirname(__file__)
shp_dir = os.path.join(os.path.dirname(thisdir), 'shapefiles')


def test_obj_init():
    graph = ModifiedTwoStepGraph(os.path.join(shp_dir, 'testershape.shp'),
                                 geoid_column='id')
    assert graph.neighbors
    assert graph.loaded_polymap
    assert graph.loaded_geodata
