import os, sys, re
from disco.core import Disco, result_iterator
from freequery.graph.links import doclinks
from freequery.document import docparse

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)
    
dumppath = sys.argv[1]
results = Disco("disco://localhost").new_job(
    name="graph_links",
    input=[dumppath],
    map_reader=docparse,
    map=doclinks).wait()

tmpoutpath = '/tmp/fq-graph-links.dot'
tmpout = open(tmpoutpath, 'w+b')

def uri_to_node_name(uri):
    return re.sub(r'[^a-zA-Z0-9_]', '', uri)

from collections import defaultdict
nodelinks = defaultdict(set) # uri->name

tmpout.write("digraph D {\n")
for uri, link_uris in result_iterator(results):
    nn = uri_to_node_name(uri)
    for link_uri in link_uris:
        linknn = uri_to_node_name(link_uri)
        if linknn:
            nodelinks[nn].add(linknn)

# only graph links to docs in the collection
for orig,dests in nodelinks.items():
    for dest in dests:
        tmpout.write('"%s" -> "%s";\n' % (orig, dest))

tmpout.write("}")
tmpout.flush()
tmpout.close()

dotoutpath = "/tmp/fq-graph-links.pdf"
os.system("dot -Tpdf -o %s %s" % (dotoutpath, tmpoutpath))
os.system("evince %s &" % dotoutpath)
