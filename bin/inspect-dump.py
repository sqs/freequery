import sys
from freequery.repository.formats import WARCParser

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

f = open(sys.argv[1], 'rb')
for doc in WARCParser(f):
    print doc.uri

