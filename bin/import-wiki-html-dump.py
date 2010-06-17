import sys, os
from freequery.document import Document
from freequery.repository import Repository


if len(sys.argv) != 3:
    print "Usage: %s <repos> <wiki>" % sys.argv[0]
    exit(1)

repospath = sys.argv[1]
wikipath = os.path.join(sys.argv[2], 'articles')

repos = Repository(repospath)

for root, dirs, files in os.walk(wikipath):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            uri = 'file://' + path
            with open(path, 'r') as ff:
                raw = ff.read()
            doc = Document(uri, raw)
            docid = repos.add(doc)
            print "%d. %s" % (docid, uri)

repos.close()

