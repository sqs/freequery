import sys
from freequery.repository.document import Document
from freequery.repository.repository import Repository


if len(sys.argv) != 4:
    print "Usage: %s <repos> <uri> <raw>" % sys.argv[0]
    exit(1)

repospath = sys.argv[1]
uri = sys.argv[2]
raw = sys.argv[3]

repos = Repository(repospath)
d = Document(uri, raw)
print repos.add(d)
repos.close()

