import sys, time
from disco.core import Disco, result_iterator
from disco.func import chain_reader
from freequery.graph.pagerank import *
from freequery.index.mapreduce import docparse

if len(sys.argv) != 2:
    print "Usage: %s <dump>" % sys.argv[0]
    exit(1)

def result_stats(results):
    o = []
    p_sum = 0.0
    for doc,__ignore in result_iterator(results):
        o.append("%f\t%s" % (doc.pagerank, doc.uri))
        p_sum += doc.pagerank
    o.append("%f\tSUM" % p_sum)
    return "\n".join(o)


dumppaths = sys.argv[1:]
disco = Disco("disco://localhost")
alpha = 0.15

results = disco.new_job(
    name="pagerank_mass0",
    input=dumppaths,
    map_reader=docparse,
    map=pagerank_mass_map,
    reduce=pagerank_mass_reduce,
    sort=True,
    params=dict(iter=0, doc_count=4)).wait()

print "Iteration 0:\n", result_stats(results)

for i in range(1,10):
    results = disco.new_job(
        name="pagerank_mass%d" % i,
        input=results,
        map_reader=chain_reader,
        map=pagerank_mass_map,
        reduce=pagerank_mass_reduce,
        sort=True,
        params=dict(iter=i)).wait()
    
    results = disco.new_job(
        name="pagerank_teleport%d" % i,
        input=results,
        map_reader=chain_reader,
        map=pagerank_teleport_map,
        sort=True,
        params=dict(iter=i, alpha=alpha, doc_count=4)).wait()
    
    print "Iteration %d:" % i
    print result_stats(results)
    time.sleep(1)
