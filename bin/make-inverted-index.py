import sys
from freequery.index.forward_index import ForwardIndex
from freequery.index.inverted_index import InvertedIndexWriter

if len(sys.argv) != 3:
    print "Usage: %s <fwdindex> <invindex>" % sys.argv[0]
    exit(1)
    
fwdindexpath = sys.argv[1]
invindexpath = sys.argv[2]

fwdindex = ForwardIndex(fwdindexpath)
iiwriter = InvertedIndexWriter(invindexpath)

i = 0
for e in fwdindex:
    iiwriter.add(e)
    print i
    i += 1

iiwriter.finish()
fwdindex.close()



