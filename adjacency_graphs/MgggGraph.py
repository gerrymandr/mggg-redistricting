import collections
from adjacency_graphs.temp_create_polymap import temp_create_polymap


class MgggGraph(object):
    """ Take in a path to a shapefile and create a graph. If an argument is provided
        for loaded_geodata, that one is used rather than one loaded with shape_dir
        Input:
            loaded_geodata (object): A geodata object as defined
                                     in loaded_geodata.
            shape_dir (string)
            geoid_column (string)

        Attributes:
            neighbors (dict): the neighbors as defined by mgg_twostep
    """

    def __init__(self, shape_dir='', geoid_column='', loaded_geodata=None):
        if loaded_geodata is not None:
            self.loaded_geodata = loaded_geodata
        else:
            self.loaded_geodata = temp_create_polymap(shape_dir, geoid_column)
        self.mggg_twostep()

    def mggg_twostep(self):
        """ Set the self.neighbors
        """
        assert self.loaded_geodata is not None
        vertices = collections.defaultdict(set)
        for i, s in self.loaded_geodata.items():
            newvertices = s.vertices[:-1]
            for v in newvertices:
                vertices[v].add(i)

        w = collections.defaultdict(set)
        for neighbors in vertices.values():
            for neighbor in neighbors:
                w[neighbor] = w[neighbor] | neighbors
        self.neighbors = w
