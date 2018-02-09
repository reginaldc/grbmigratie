# grbmigratie
Dit project heeft als doelstelling de migratie van  Cadmap naar het GRB te vergemakkelijken.
Bouwdossiers en verkavelingen dienen te worden ingetekend op het GRB.
Veel gemeenten hebben met dit proces gewacht tot de kadastralisatie een feit is.
Kadastralisatie is het bijwerken van de achterkant van bebouwde percelen aan de hand van luchtfotos.
Dit script heeft als doel om de bouwdossiers die gelegen zijn op percelen die weinig afwijken in het GRB (ten opzichte van het kadaster)
automatisch goed te zetten.
Het sript bouwaanvragen_ok.py is een script dat moet worden uitgevoerd in de python console van qgis.
Volgende lagen dienen aanwezig te zijn bij het uitvoeren hiervan:
-	Bouwaanvragen_ok: laag met de bouwdossiers die automatisch kunnen gemigreerd worden
-	ADP: laag met de adppolygonen die zullen dienen om de bouwdossiers in te tekenen
-	Intersectielaag: laag gevormd door intersectie van de perceelnummers (verrijkt met capakey en opp) met de bouwdossiers, met eventueel daaraan toegevoegd Ratio en Ratio_N
