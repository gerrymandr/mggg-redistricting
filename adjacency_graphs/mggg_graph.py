import pandas as pd


class MgggGraph(object):
    """ This is an object to store and modify reusable graph attributes in
        python. All algorithm functions should return a MgggGraph object.

        Attributes/Inputs:
            shp_path (string): A string 'path/to/shapefile.shp`.
            id_column (string): The name of the column which gives vertex id
            shape_df (pd.DataFrame): The dataframe associated to the vertices.
            loaded_geodata (): Output of pysal.open(shp_path)
            loaded_polymap (dict): Shape data in a standard python format.
            neighbors (dict): Keys are vertices, values are a list of 
                              associated vertices.

        Methods:
            export_graph(self, output_path): Export to csv at output_path
            add_edge:(self, tuple[int, int]): Add edge between (i, j)
            drop_edge:(self, tuple[int, int]): Drop edge between (i, j)
            add_vertex:

    """

    def __init__(self,
                 shp_path='', id_column='', shape_df=None,
                 loaded_geodata=None, loaded_polymap=None,
                 neighbors=None):
        self.shp_path = shp_path
        self.id_column = id_column
        self.shape_df = shape_df
        self.loaded_geodata = loaded_geodata
        self.loaded_polymap = loaded_polymap
        self.neighbors = neighbors

    def export_graph(self, output_path='graph.csv'):
        """ Export csv to output_path.
        """
        data_shape = self.shape_df
        data_shape = data_shape.drop('geometry', 1)

        data_neighbors = self.neighbors
        adjacency_df = pd.DataFrame(columns=[self.id_column, 'vertices'])
        for item in data_neighbors.items():
            adjacency_df = adjacency_df.append(
                pd.DataFrame(columns=[self.id_column, 'vertices'],
                             data=[[item[0], item[1]]])
            )
        data = data_shape.merge(adjacency_df,
                                on=self.id_column, how='outer')
        data.to_csv(output_path)

    def drop_edge(self, edge):
        """ Modify the neighbors attribute to remove one edge.
        """
        assert len(edge) == 2
        gph_edges = self.neighbors

        assert edge[0] in gph_edges[edge[1]]
        assert edge[1] in gph_edges[edge[0]]

        gph_edges[edge[0]].remove(edge[1])
        gph_edges[edge[1]].remove(edge[0])
        self.neighbors = gph_edges

    def add_edge(self, edge):
        """ Modify the neighbors attribute to add one edge
        """
        assert len(edge) == 2
        gph_edges = self.neighbors

        assert edge[0] not in gph_edges[edge[1]]
        assert edge[1] not in gph_edges[edge[0]]

        gph_edges[edge[0]].add(edge[1])
        gph_edges[edge[1]].add(edge[0])
        self.neighbors = gph_edges
