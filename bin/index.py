"""
Indexes a Web dump file given as a command-line argument.
"""

import sys

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

from discodex.client import DiscodexClient
from discodex.objects import DataSet

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

dumpfile = sys.argv[1]
ds = DataSet(input=[dumpfile],
             options=dict(parser='freequery.index.mapreduce.docparse',
                          demuxer='freequery.index.mapreduce.docdemux'))

client = DiscodexClient()
orig_spec = client.index(ds)
client.clone(orig_spec, 'fqinvindex')
