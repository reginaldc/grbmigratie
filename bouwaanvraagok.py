from PyQt4.QtCore import *
from qgis.core import (QgsFeature, QgsField, QgsFields,
                       QgsGeometry, QgsPoint, QgsVectorFileWriter)
                       
layers = iface.legendInterface().layers()

# Define a custom `key` function for use with `sorted`
# which is passed a feature `f` and returns the value
# of it's `name` attribute
def get_name(f):
    return f['dossiernr']

# Create a sorted list of features. The `sorted` function
# will read all features into a list and return a new list
# sorted in this case by the features name value returned
# by the `get_name` function
#pnr is de laag bekomen door intersectie van perceelnummers met bouwdossiers
features = None
adpfeatures = None
adplyr = None
for lyr in layers:
        if lyr.name() == "pnr":
            features = sorted(lyr.getFeatures(), key=get_name)
        if lyr.name() == "ADP36007":
            adpfeatures = lyr.getFeatures()
            adplyr = lyr
            
# Loop through the sorted list and print out the name value
# of each just to prove it's now sorted.
dosstemp = "temp"
geomtemp = None
fields = QgsFields()
fields.append(QgsField("CEVI_OID", QVariant.Int))
fields.append(QgsField("CEVI_DATE_CREATED",QVariant.DateTime))
fields.append(QgsField("CEVI_USERID_CREATED",QVariant.String))
fields.append(QgsField("CEVI_DATE_UPDATED",QVariant.DateTime))
fields.append(QgsField("DOSSIER",QVariant.Double))
fields.append(QgsField("DOSSIERNR",QVariant.String))
fields.append(QgsField("DOSSIERTP",QVariant.String))

writer = QgsVectorFileWriter("dossiers.shp","utf_8_encode",fields,QGis.WKBMultiPolygon,None,"ESRI Shapefile")
for feature in features:
    checkdossier = 0
    tel = 0
    while checkdossier != 1:
        capakey = feature["capakey"]
        oid = feature["cevi_oid"]
        created = feature["cevi_date_created"]
        userid = feature["cevi_userid_created"]
        updated = feature["cevi_date_updated"]
        doss = feature["dossier"]
        dosstp = feature["dossiertp"]
        nr = feature["dossiernr"]
        geom = None
        print (capakey)
        if dosstemp == nr:
            print("eerste doorloop")
            #dossier met meerdere percelen
            dosstemp = feature['dossiernr']            
            exp = QgsExpression("\"CAPAKEY\" = "+ capakey + "  ")
            request = QgsFeatureRequest(exp)
            adpf = adplyr.getFeatures(request)            
            for ad in adpf:
                print("feature gevonden")
                geom = QgsGeometry(ad.constGeometry())            
            geomtemp = geomtemp.combine(geom)
            tel += 1
        else:
            print("in de andere routine")
            dosstemp = feature['dossiernr']            
            exp = QgsExpression("\"CAPAKEY\" = " + capakey + " ")
            request = QgsFeatureRequest(exp)
            adpf = adplyr.getFeatures(request)
            for ad in adpf:
                ("feature aanwezig")
                geom = QgsGeometry(ad.constGeometry()) 
            if tel >= 1:
                geomtemp = geomtemp.combine(geom)
                checkdossier = 1
            else:
                geomtemp = geom
                tel +=1
    # schrijf geometrie en dossiergegevens naar dossierlaag
    fet = QgsFeature()
    fet.setGeometry(geomtemp)
    fet.setAttributes([oid, created,userid,updated,doss,nr,dosstp])
    writer.addFeature(fet)
    