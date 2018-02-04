import os

from adjacency_graphs.algorithms import TwoStepGraph

thisdir = os.path.dirname(__file__)
shp_dir = os.path.join(os.path.dirname(thisdir), 'shapefiles')


def test_obj_init():
    graph = TwoStepGraph(os.path.join(shp_dir, 'testershape.shp'),
                         id_column='id')
    assert graph.shp_path
    assert graph.id_column
    assert graph.loaded_geodata
    assert graph.loaded_polymap
    assert graph.neighbors
