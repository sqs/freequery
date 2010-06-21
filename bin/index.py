"""
Indexes a Web dump file given as a command-line argument.
"""

import sys, commands

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

print commands.getoutput("echo '%s' | discodex index --parser " \
                         "freequery.index.mapreduce.docparse" % sys.argv[1])
