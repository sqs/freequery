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
    for k,v in result_iterator(results):
        if hasattr(k, 'pagerank'):
            doc = k
            o.append("%f\t%s" % (doc.pagerank, doc.uri))
            p_sum += doc.pagerank
        else:
            o.append("%f\t(dangling mass)" % v)
            p_sum += v
    o.append("%f\tSUM" % p_sum)
    return "\n".join(o)


dumppaths = sys.argv[1:]
disco = Disco("disco://localhost")
alpha = 0.15
doc_count = 4

results = disco.new_job(
    name="pagerank_mass0",
    input=dumppaths,
    map_reader=docparse,
    map=pagerank_mass_map,
    reduce=pagerank_mass_reduce,
    sort=True,
    params=dict(iter=0, doc_count=doc_count)).wait()

print "Iteration 0:\n", result_stats(results)

i = 0
while i < 10:
    # get sum of dangling node pageranks
    for k,v in result_iterator(results):
        print "%r,%r" % (k,v)
    lost_mass = sum(v for k,v in result_iterator(results) \
                      if k == DANGLING_MASS_KEY)
    
    results = disco.new_job(
        name="pagerank_teleport_distribute%d" % i,
        input=results,
        map_reader=chain_reader,
        map=pagerank_teleport_distribute_map,
        sort=True,
        params=dict(iter=i, alpha=alpha, doc_count=doc_count,
                    lost_mass_per=float(lost_mass)/doc_count)
    ).wait()
    
    print "Iteration %d:" % i
    print result_stats(results)
    print "Lost mass: %f" % lost_mass
    i += 1
    time.sleep(1)

    results = disco.new_job(
        name="pagerank_mass%d" % i,
        input=results,
        map_reader=chain_reader,
        map=pagerank_mass_map,
        reduce=pagerank_mass_reduce,
        sort=True,
        params=dict(iter=i)).wait()

