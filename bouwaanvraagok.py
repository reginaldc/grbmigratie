import pymssql

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

fields = [QgsField("CEVI_OID", QVariant.Int),
            QgsField("CEVI_DATE_CREATED",QVariant.DateTime),
            QgsField("CEVI_USERID_CREATED",QVariant.String),
            QgsField("CEVI_DATE_UPDATED",QVariant.DateTime),
            QgsField("DOSSIER",QVariant.Double),
            QgsField("DOSSIERNR",QVariant.String),
            QgsField("DOSSIERTP",QVariant.String)]
writer = QgsVectorFileWriter("F:\QGIS\output\dossiers.shp","31370",fields,QGis.WKBPoligon,"ESRI Shapefile")
for feature in features:
    checkdossier = 0
    tel = 0
    while checkdossier != 1:
        capakey = feature["capa"]
        oid = feature["cevi_oid"]
        created = feature["cevi_date_created"]
        userid = feature["cevi_userid_created"]
        updated = feature["cevi_date_updated"]
        doss = feature["dossier"]
        dosstp = feature["dossiertp"]
        nr = feature["dossiernr"]
        
        if dosstemp == nr:
            #dossier met meerdere percelen
            dosstemp = feature['dossiernr']
            exp = QgsExpression("CAPAKEY ILIKE %s",capakey)
            request = QgsFeatureRequest(exp)
            adpf = adplyr.getFeatures(request)
            geom = QgsGeometry(adpf.constGeometry())
            geomtemp = geomtemp.combine(geom)
            tel += 1
        else:
            dosstemp = feature['dossiernr']
            exp = QgsExpression("CAPAKEY ILIKE %s",capakey)
            request = QgsFeatureRequest(exp)
            adpf = adplyr.getFeatures(request)
            geom = QgsGeometry(adpf.constGeometry())
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
    