"""
perform tract-level computations
"""
# import the library functions
from district_node_computation_library import *

# define parameters
# using 2010 tract data
shp_and_dbf_file_dir = "/Users/avelez/Documents/MGGG_UROP/data/shapefile_data/tract_file"

# using 2013 congressional district data
cd_dbf_dir = "/Users/avelez/Documents/MGGG_UROP/data/shapefile_data/cb_2013_us_cd113_500k.dbf"
cd_shp_dir = "/Users/avelez/Documents/MGGG_UROP/data/shapefile_data/cb_2013_us_cd113_500k.shp"

sub_geoid_col = 'GEOID10'
cd_col = 'GEOID'
state_col = 'STATEFP'
begin = -14
end = -12
shp_name = "tracts.shp"

# obtain the lists-of-lists
entries, node_membership = get_district_member_and_boundary_entities(shp_and_dbf_file_dir, cd_dbf_dir, cd_shp_dir, sub_geoid_col, cd_col, state_col, begin, end, shp_name)

df_entries = pd.DataFrame(entries)
df_node_membership = pd.DataFrame(node_membership)

df_entries.to_csv("district_to_tracts_overlap_new.csv", index=False, header = False)
df_node_membership.to_csv("tract_membership_new.csv", index=False,header=False)
