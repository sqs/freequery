import os, sys
from freequery.document import Document
from freequery.repository.formats import WARCWriter

if len(sys.argv) != 2:
    print "Usage: %s <wiki-path>" % sys.argv[0]
    exit(1)

    
wikipath = os.path.join(sys.argv[1], 'articles')

dump_writer = WARCWriter(sys.stdout)

for root, dirs, files in os.walk(wikipath):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'rb') as ff:
                raw = ff.read()
            doc = Document(path, raw)
            dump_writer.write(doc)
            sys.stderr.write(path + "\n")
