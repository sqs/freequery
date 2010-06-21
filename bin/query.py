import sys, commands

if len(sys.argv) != 2:
    print "Usage: %s <query>" % sys.argv[0]
    exit(1)

query = sys.argv[1]

print commands.getoutput("discodex query fq %s" % query)

