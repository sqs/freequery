import sys
from freequery.repository.repository import Repository
from freequery.index.inverted_index import InvertedIndexReader

if len(sys.argv) != 4:
    print "Usage: %s <repos> <invindex> <term>" % sys.argv[0]
    exit(1)

repospath = sys.argv[1]
invindexpath = sys.argv[2]
term = sys.argv[3]

repos = Repository(repospath)
invindex = InvertedIndexReader(invindexpath)

docids = map(lambda p: p.docid, invindex.lookup(term))
for docid in docids:
    print repos.get(docid).uri

repos.close()
invindex.close()



