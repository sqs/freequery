import sys
from discodex.client import DiscodexClient
from discodex.objects import DataSet
from freequery.index.mapreduce import docparse
from freequery.graph.links import doclinkdemux

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

dumpfile = sys.argv[1]
ds = DataSet(input=[dumpfile],
             options=dict(parser='freequery.index.mapreduce.docparse',
                          demuxer='freequery.graph.links.doclinkdemux'))

client = DiscodexClient()
orig_spec = client.index(ds)
client.clone(orig_spec, 'fqlinks')

