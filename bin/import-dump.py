import sys
from freequery.document import Document
from freequery.repository import Repository


if len(sys.argv) != 3:
    print "Usage: %s <repos> <dump>" % sys.argv[0]
    exit(1)

repospath = sys.argv[1]
dumppath = sys.argv[2]

repos = Repository(repospath)
dumpfile = open(dumppath, 'rb')

DELIM = "@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@\n"
ST_URI = 0
ST_META = 1
ST_RAW = 2
state = ST_URI

uri = None
s = []
for line in dumpfile:
    if state == ST_URI:
        uri = line.strip()
        state = ST_META
    elif state == ST_META:
        if line == "\n":
            state = ST_RAW
    elif state == ST_RAW:
        if line != DELIM:
            s.append(line)
        else:
            d = Document(uri, ''.join(s))
            docid = repos.add(d)
            print "%d\t%s" % (docid, uri)
            uri = None
            s = []
            state = ST_URI

dumpfile.close()
