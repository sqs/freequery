import sys
from freequery.repository.repository import Repository

if len(sys.argv) != 3:
    print "Usage: %s <repos> <docid>" % sys.argv[0]

repospath = sys.argv[1]
docid = int(sys.argv[2])

repos = Repository(repospath)
doc = repos.get(docid).make_typed('text/html')

print "URI: %s" % doc.uri
print "Raw: (%d bytes)" % len(doc.raw)

print "Term hits:"
for (term,hits) in doc.term_hits().items():
    print " - %s (x%d)" % (term, len(hits))

