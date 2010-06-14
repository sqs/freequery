import sys
from freequery.repository.repository import Repository

if len(sys.argv) != 2:
    print "Usage: %s <repos>" % sys.argv[0]

repospath = sys.argv[1]
repos = Repository(repospath)

for doc in repos:
    print "%06d\t%s\n      \tsize=%d" % (doc.docid, doc.uri, len(doc.raw))

repos.close()
