import collections


class MgggGraph(object):
    """ Take in a path to a shapefile and create a graph.
        Input:
            loaded_geodata (object): A geodata object as defined
                                     in loaded_geodata.

        Attributes:
            neighbors (dict): the neighbors as defined by mgg_twostep
    """

    def __init__(self, loaded_geodata=None):
        self.loaded_geodata = loaded_geodata

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
