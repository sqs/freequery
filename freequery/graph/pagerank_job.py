from disco.core import Disco
from freequery.repository.docset import Docset
from freequery.graph.pagerank import DANGLING_MASS_KEY

class PagerankJob(object):

    def __init__(self, spec, disco_addr="disco://localhost",
                 alpha=0.15, niter=2):
        self.spec = spec
        self.docset = Docset(spec.docset_name)
        self.disco = Disco("disco://localhost")
        self.alpha = alpha
        self.niter = niter
        self.doc_count = 31875 # TODO: don't hardcode
        self.nr_partitions = 16
        self.merge_partitions = False
        self.mem_sort_limit = 1024*1024*1024*1.5 # 1.5 GB

    def start(self):
        from disco.core import result_iterator
        from disco.func import chain_reader
        from freequery.index.mapreduce import docparse
        from freequery.graph.pagerank import pagerank_mass_map, \
            pagerank_mass_reduce, pagerank_teleport_distribute_map, \
            pagerank_partition

        results = self.disco.new_job(
            name="pagerank_mass0",
            input=self.docset.dump_uris(),
            map_reader=docparse,
            map=pagerank_mass_map,
            reduce=pagerank_mass_reduce,
            sort=True,
            partitions=self.nr_partitions,
            partition=pagerank_partition,
            merge_partitions=self.merge_partitions,
            mem_sort_limit=self.mem_sort_limit,
            params=dict(iter=0, doc_count=self.doc_count)).wait()
        ## print "Iteration 0:\n", self.__result_stats(results)

        for i in range(1, self.niter+1):
            # get sum of dangling node pageranks
            lost_mass = sum(v for k,v in result_iterator(results) \
                              if k == DANGLING_MASS_KEY)
    
            results = self.disco.new_job(
                name="pagerank_teleport_distribute%d" % (i-1),
                input=results,
                map_reader=chain_reader,
                map=pagerank_teleport_distribute_map,
                sort=True,
                partitions=self.nr_partitions,
                partition=pagerank_partition,
                merge_partitions=self.merge_partitions,
                mem_sort_limit=self.mem_sort_limit,
                params=dict(iter=i, alpha=self.alpha,
                            doc_count=self.doc_count,
                            lost_mass_per=float(lost_mass)/self.doc_count)
            ).wait()
    
            ## print "Iteration %d:" % i
            ## print self.__result_stats(results)
            ## print "Lost mass: %f" % lost_mass

            results = self.disco.new_job(
                name="pagerank_mass%d" % i,
                input=results,
                map_reader=chain_reader,
                map=pagerank_mass_map,
                reduce=pagerank_mass_reduce,
                sort=True,
                partitions=self.nr_partitions,
                partition=pagerank_partition,
                merge_partitions=self.merge_partitions,
                mem_sort_limit=self.mem_sort_limit,
                params=dict(iter=i)).wait()

        # write scoredb
        from freequery.graph.scoredb import ScoreDBWriter
        from freequery.document import Document
        db = ScoreDBWriter(self.spec.scoredb_path)
        score_iter = ((doc.uri, doc.pagerank) for doc,_
                      in result_iterator(results) if isinstance(doc, Document))
        db.set_scores(score_iter)
        db.save_and_close()            

    def __result_stats(self, results):
        from disco.core import result_iterator
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
