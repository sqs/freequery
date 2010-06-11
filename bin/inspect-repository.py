import sys
from freequery.repository.repository import Repository

if len(sys.argv) != 2:
    print "Usage: %s <repos>" % sys.argv[0]

repospath = sys.argv[1]
repos = Repository(repospath)

for docid in repos.docindex.docids():
    doc = repos.get(docid)
    print "%06d\t%s\n      \tsize=%d" % (docid, doc.uri, len(doc.data['orig']))

repos.close()
