def export_graph(mggg_graph, output_path='graph.csv'):
    data = mggg_graph.shape_df
    data.to_csv(output_path)
