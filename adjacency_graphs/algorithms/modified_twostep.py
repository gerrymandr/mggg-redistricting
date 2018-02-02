import collections
import pysal as ps


def _create_polymap(shp_path, pysal_shp_obj, geoid_column):
    split = shp_path.split('.')
    split[-1] = 'dbf'
    dbf_dir = '.'.join(split)
    dbf = ps.open(dbf_dir)

    geoid_list = dbf.by_col_array(geoid_column)
    geom_list = [x for x in pysal_shp_obj]
    return {geoid_list[i][0]: geom_list[i] for i in range(len(geom_list))}


def _modified_twostep(polymap):
    shpFileObject = polymap
    # if shpFileObject.type != ps.cg.Polygon:
    # 	return
    numPoly = len(shpFileObject)

    vertices = collections.defaultdict(set)
    for i, s in shpFileObject.items():
        newvertices = s.vertices[:-1]
        for v in newvertices:
            vertices[v].add(i)

    w = collections.defaultdict(set)
    for neighbors in vertices.values():
        for neighbor in neighbors:
            w[neighbor] = w[neighbor] | neighbors
    return w


# TODO: it might be nice to use abstract base classes here to define a
#       standard interface that all Graph objects should follow.
class ModifiedTwoStepGraph(object):
    """Take in a path to a shapefile and create a graph. If a pysal object
        (loaded from a shapefile) is given for the loaded_geodata argument,
        that object is used instead of any shp_path argument.

        Analysis of adjacency is done with the two-step
        algorithm defined in
        https://github.com/gerrymandr/state-adjacency-graphs/blob/master/scipy_conference_scaling_adjacency_algos.pdf

        Input:
            loaded_geodata (object): A pysal-created object from opening a
                   shp file
            shp_path (string):
            geoid_column (string): required if using shapedir, not
                   loaded_geodata

        Attributes:
            neighbors (dict): the neighbors as defined by mgg_twostep
            loaded_geodata: the pysal object representing the shp_path
            loaded_polymap: a polymap generated from loaded_geodata

    """

    def __init__(self, shp_path='', geoid_column='', loaded_geodata=None):
        if loaded_geodata is not None:
            self.loaded_geodata = loaded_geodata
        else:
            self.loaded_geodata = ps.open(shp_path)
            self.loaded_polymap = _create_polymap(shp_path,
                                                  self.loaded_geodata,
                                                  geoid_column)
        self.neighbors = _modified_twostep(self.loaded_polymap)
