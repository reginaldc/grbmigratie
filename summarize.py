from osgeo import ogr
from PyQt4.QtCore import *
from qgis.core import (QgsFeature, QgsField, QgsFields,
                       QgsGeometry, QgsPoint, QgsVectorFileWriter)

source = ogr.Open('F:\\Gis\\project\\Extracted\\bouwaanvragenbis.shp', update=True)
layer = source.GetLayer()

new_field = ogr.FieldDefn('SUM', ogr.OFTInteger)
layer.CreateField(new_field)
source = None
lyr = QgsVectorLayer('F:\\Gis\\project\\Extracted\\bouwaanvragenbis.shp', 'bouwaanvragenbis', 'ogr')
QgsMapLayerRegistry.instance().addMapLayer(lyr)


# Define a custom `key` function for use with `sorted`
# which is passed a feature `f` and returns the value
# of it's `name` attribute
def get_name(f):
    return f['DOSSIERNR']

# Create a sorted list of features. The `sorted` function
# will read all features into a list and return a new list
# sorted in this case by the features name value returned
# by the `get_name` function
features = sorted(lyr.getFeatures(), key=get_name)
f_prev = None
count = 1
lyr.startEditing()
for f in features:
    f_prev = f["DOSSIERNR"]
    fnext = features.next()
    if f_prev == fnext["DOSSIERNR"]:
        count += 1
        f["SUM"] = count
        lyr.updateFeature(f)
    else:
        f_prev = fnext["DOSSIERNR"]
        f["SUM"] = count
        count = 1
lyr.commitChanges()