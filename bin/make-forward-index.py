import sys
from freequery.repository.repository import Repository
from freequery.index.forward_index import ForwardIndex

if len(sys.argv) not in (3,4,5):
    print "Usage: %s <repos> <fwdindex> [start-docid [end-docid]]" % sys.argv[0]
    exit(1)
    
repospath = sys.argv[1]
fwdindexpath = sys.argv[2]
start_docid = int(sys.argv[3])
end_docid = int(sys.argv[4])

repos = Repository(repospath)
fwdindex = ForwardIndex(fwdindexpath)

i = 1
for doc in repos:
    if doc.docid in range(start_docid, end_docid+1):
        doc.make_typed('text/html')
        print "%d. %s" % (i, doc.uri)
        fwdindex.add(doc)
        i += 1
    elif doc.docid > end_docid:
        break

fwdindex.close()
repos.close()



