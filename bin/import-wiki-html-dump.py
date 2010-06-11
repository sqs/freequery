import sys, os
from freequery.repository.repository import Repository
from freequery.repository.document import Document

if len(sys.argv) != 3:
    print "Usage: %s <repos> <wiki>" % sys.argv[0]
    exit(1)

repospath = sys.argv[1]
wikipath = os.path.join(sys.argv[2], 'articles')

repos = Repository(repospath)
i = 1

for root, dirs, files in os.walk(wikipath):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            uri = 'file://' + path
            with open(path, 'r') as ff:
                raw = ff.read()
            doc = Document(uri, raw)
            repos.add(doc)
            print "%d. %s" % (i, uri)
            i += 1

repos.close()

