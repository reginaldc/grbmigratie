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
conn = pymssql.connect("SQLCEVI","xxxx","xxxx","SQLSPATIAL")
cursor = conn.cursor()
fields = [QgsField("CEVI_OID", QVariant.Int),QgsField("CEVI_DATE_CREATED",QVariant.DateTime),QgsField("CEVI_USERID_CREATED",QVariant.String),QgsField("CEVI_DATE_UPDATED",QVariant.DateTime),QgsField("DOSSIER",QVariant.Double),QgsField("DOSSIERNR",QVariant.String),QgsField("DOSSIERTP",QVariant.String)]
writer = QgsVectorFileWriter("F:\QGIS\output\dossiers.shp","31370",fields,QGis.WKBPoligon,"ESRI Shapefile")
for feature in features:
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
        #code voor het combineren van percelen
        cursor.execute("SELECT * from ADP36007 WHERE CAPAKEY LIKE %s", capakey)
        row = cursor.fetchone()
        geom = row["GEOMETRY"]
    else:
        dosstemp = feature['dossiernr']
        # selecteer perceel in ADP met capakey
        cursor.execute("SELECT * from ADP36007 WHERE CAPAKEY LIKE %s", capakey)
    row = cursor.fetchone()
    geom = row["GEOMETRY"]
    