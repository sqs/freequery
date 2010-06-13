import sys
from freequery.index.forward_index import ForwardIndex
from freequery.index.inverted_index import InvertedIndex

if len(sys.argv) != 3:
    print "Usage: %s <fwdindex> <invindex>" % sys.argv[0]
    exit(1)
    
fwdindexpath = sys.argv[1]
invindexpath = sys.argv[2]

fwdindex = ForwardIndex(fwdindexpath)
invindex = InvertedIndex(invindexpath)

i = 0
for e in fwdindex:
    invindex.add(e)
    print i
    i += 1


invindex.save()
invindex.close()
fwdindex.close()



