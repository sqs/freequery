import sys
from freequery.document import Document
from freequery.formats.warc import WARCWriter

if len(sys.argv) != 2:
    print "usage: %s <uri>" % sys.argv[0]
    exit(1)

doc = Document(sys.argv[1], sys.stdin.read())
writer = WARCWriter(sys.stdout)
writer.write(doc)
