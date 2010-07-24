import sys
from freequery.repository.formats import WARCParser, WARCWriter

infile = open(sys.argv[1], 'rb')
uri = sys.argv[2]

for doc in WARCParser(infile):
    if doc.uri == uri:
        w = WARCWriter(sys.stdout)
        w.write(doc)
        break
