import sys
from freequery.repository.formats import WARCParser

for doc in WARCParser(open(sys.argv[1], 'rb')):
    print doc.uri
    for uri in doc.link_uris():
        pass#print " - %s" % uri
