#!/usr/bin/env python

from rdflib import URIRef, Literal, Graph
from rdflib.namespace import SKOS
import gspread

# Graph
g = Graph()

# Google spreadsheets login
gc = gspread.login('albert.meronyo@gmail.com', 
                   'Civ33a4kXuc22l3j')

# Open worksheet
wb = gc.open("Links HISCO and ICONCLASS")
wks = wb.get_worksheet(2)

# Fetch the data
icURIs = wks.col_values(4)
icDescs = wks.col_values(3)
hiscoURIs = wks.col_values(7)
hiscoDescs = wks.col_values(6)

linkCount = 0
for i in range(2,len(icURIs)-1):
    try:
        icURI = URIRef(icURIs[i])
    except:
        continue
    icDesc = Literal(icDescs[i])
    try:
        hiscoURI = URIRef("http://cedar.example.org/ns#hisco-" + hiscoURIs[i])
    except:
        continue
    hiscoDesc = Literal(hiscoDescs[i])

    print icURI, icDesc, hiscoURI, hiscoDesc
    g.add( (icURI, SKOS.prefLabel, icDesc) )
    g.add( (icURI, SKOS.exactMatch, hiscoURI) )
    g.add( (hiscoURI, SKOS.prefLabel, hiscoDesc) )
    linkCount += 1

g.serialize('gspread-ic-hisco.ttl', format="turtle")
print "Serialized %s links" % str(linkCount)


