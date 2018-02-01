## Target tasks

1. load shapefile and accompanying dbf file (associate district id, geoID)
2. compute adjacency (twostep algorithm).  Output mutable object representing graph.
3. provide methods for manually modifying adjacency entries
4. save/load graph objects
5. plot graph objects overlaid with/without district boundary data


## Current code

compute_tract_membership_and_overlap_with_districts.py:
  * twostep
  * modified_twostep
  * using pandas to open .dbf file
  * building district-to-geoid map from .dbf
  * compute tract membership in district (buffer method)
  
  
adj_graph_map_layer.py:
  * create shapefile from csv data
  

adj_matrix_gen.py:
  * tabulate/aggregate adjacency files
  
  
district_node_computation_library.py:
  * create_polymap (input shp_dir, dbf_dir, geoid_column)
  * get_dbf_shp_files(directory)
  * mggg_twostep(polymap)
  * visualize_adjacency_graph(file_dir, out_dir=None)
  
block_groups.py:
  * run orchestration of district_node_computation_library.get_district_member_and_boundary_entities
  * write overlap/membership CSVs
 
 
tracts.py:
  * same as block_groups.py, with different inputs

