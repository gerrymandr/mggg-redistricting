# https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#create-point-shapefile-with-attribute-data

# Parse a delimited text file of volcano data and create a shapefile
import osgeo.ogr as ogr
import osgeo.osr as osr
import csv

# use a dictionary reader so we can access by field name
# TODO: NEED A FILE FOR THIS
reader = csv.DictReader(open("volcano_data.txt", "rb"),
                        delimiter='\t',
                        quoting=csv.QUOTE_NONE)

# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

# create the data source
# TODO: FIX THIS, or use some existing shapefile??
data_source = driver.CreateDataSource('volcanoes.shp')

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer_name = "{}_adj_graph".format('district')
layer = data_source.CreateLayer(layer_name, srs, ogr.wkbPoint)

# Add the fields we're interested in
# TODO: DOES THIS NEED FIELDS?
field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)
field_region = ogr.FieldDefn("Region", ogr.OFTString)
field_region.SetWidth(24)
layer.CreateField(field_region)
layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Elevation", ogr.OFTInteger))

# Process the text file and add the attributes and features to the shapefile
for row in reader:
    # create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    # Set the attributes using the values from the delimited text file
    feature.SetField("Name", row['Name'])
    feature.SetField("Region", row['Region'])
    feature.SetField("Latitude", row['Latitude'])
    feature.SetField("Longitude", row['Longitude'])
    feature.SetField("Elevation", row['Elev'])

    # create line between centers of tracts?
    # TODO: MAKE REFERENCES FOR THESE NUMBERS. GENERALLY HAVE DATA SOURCE
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(1116651.439379124, 637392.6969887456)
    line.AddPoint(1188804.0108498496, 652655.7409537067)

    # Set the feature geometry using the line
    feature.SetGeometry(line)
    # Create the feature in the layer (shapefile)
    layer.CreateFeature(feature)
    # Dereference the feature
    feature = None

# Save and close the data source
data_source = None
