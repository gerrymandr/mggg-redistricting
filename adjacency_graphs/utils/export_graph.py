def export_graph(mggg_graph, output_path='graph.csv'):
    data_shape = mggg_graph.shape_df
    data_neighbors = mggg_graph.neighbors
    # Adjacency dataframe
    adjacency_df = pd.DataFrame(columns=['GEOID', 'vertices'])
    for item in data_neighbors.items():
        adjacency_df = adjacency_df.append(pd.DataFrame(columns=['GEOID', 'vertices'], 
                                                        data=[[item[0], item[1]]]))
    # Adding adjacency data to dataframe.
    data = data_shape.merge(adjacency_df, on='GEOID', how='outer')
    data.to_csv(output_path)
