import sys
from freequery.repository.formats import QTableFile

for doc in QTableFile(open(sys.argv[1], 'rb')):
    print doc.uri
    for uri in doc.link_uris():
        print " - %s" % uri
