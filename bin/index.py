"""
Indexes a Web dump file given as a command-line argument.
"""

import sys, commands

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

index_id = commands.getoutput(
    "echo '%s' | discodex index --parser freequery.index.mapreduce.docparse " \
    "--demuxer freequery.index.mapreduce.docdemux " \
    % sys.argv[1])

print commands.getoutput("discodex clone %s fq" % index_id)
