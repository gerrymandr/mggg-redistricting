import pysal as ps


def temp_create_polymap(shp_dir, geoid_column):
    split = shp_dir.split('.')
    split[-1] = 'dbf'
    dbf_dir = '.'.join(split)
    shp = ps.open(shp_dir)
    dbf = ps.open(dbf_dir)

    geoid_list = dbf.by_col_array(geoid_column)
    geom_list = [x for x in shp]
    return {geoid_list[i][0]: geom_list[i] for i in range(len(geom_list))}
