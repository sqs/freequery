import sys
from freequery.repository.repository import Repository
from freequery.repository.document_index import DocumentIndex
from freequery.index.inverted_index import InvertedIndex

if len(sys.argv) not in (3,4,5):
    print "Usage: %s <repos> <invindex> [start-docid [end-docid]]" % sys.argv[0]
    exit(1)
    
repospath = sys.argv[1]
invindexpath = sys.argv[2]
start_docid = int(sys.argv[3])
end_docid = int(sys.argv[4])

repos = Repository(repospath)
invindex = InvertedIndex(invindexpath)

i = 1
for doc in repos:
    if doc.docid in range(start_docid, end_docid+1):
        doc.make_typed('text/html')
        print "%d. %s" % (i, doc.uri)
        invindex.add((doc,))
        i += 1

invindex.save()
invindex.close()
repos.close()



