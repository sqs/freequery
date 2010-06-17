import sys
from freequery.repository import DocumentIndex
from freequery.index import ForwardIndex

if len(sys.argv) != 3:
    print "Usage: %s <docindex> <fwdindex>" % sys.argv[0]
    exit(1)

docindexpath = sys.argv[1]
fwdindexpath = sys.argv[2]
docindex = DocumentIndex(docindexpath) # for looking up docID -> URI
fwdindex = ForwardIndex(fwdindexpath)

i = 0
for e in fwdindex:
    print "%d: %s" % (e.docid, docindex[e.docid].uri)
    for th in e.term_hits:
        print "  %s: %s" % \
              (th.term, ' '.join(map(lambda h: str(h.pos), th.hits)))
    i += 1

print "\n%d entries total" % i

fwdindex.close()
