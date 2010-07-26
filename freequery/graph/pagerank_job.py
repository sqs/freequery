from disco.core import Disco
from disco.core import result_iterator
from disco.func import chain_reader
from freequery.graph.links import doclinksparse
from freequery.graph.pagerank import pagerank_mass_map, \
    pagerank_mass_reduce, pagerank_teleport_distribute_map, \
    pagerank_partition
from freequery.repository.docset import Docset
from freequery.graph.pagerank import DANGLING_MASS_KEY
from freequery.index.scoredb import ScoreDBWriter
from freequery.document import Document


class PagerankJob(object):

    def __init__(self, spec, disco_addr="disco://localhost",
                 alpha=0.15, niter=2, profile=False):
        self.spec = spec
        self.docset = Docset(spec.docset_name)
        self.disco = Disco("disco://localhost")
        self.alpha = alpha
        self.niter = niter
        self.nr_partitions = 16
        self.merge_partitions = False
        self.profile = profile

    def start(self):
        results = self.__first_mass_job()
        results = self.__teleport_distribute_job(0, results)
        for i in range(1, self.niter+1):
            #print "Iteration %d:" % (i - 1)
            #print self.__result_stats(results)
            results = self.__mass_job(i, results)
            results = self.__teleport_distribute_job(i, results)            
        self.__write_scores(results)

    def __write_scores(self, results):
        db = ScoreDBWriter(self.spec.scoredb_path)
        score_iter = ((doc.uri, doc.pagerank) for doc,_
                      in result_iterator(results) if isinstance(doc, Document))
        db.set_scores(score_iter)
        db.save_and_close()            

    def __run_job(self, job):
        results = job.wait()
        if self.profile:
            self.__profile_job(job)
        return results
        
    def __first_mass_job(self):
        return self.__run_job(self.disco.new_job( 
            name="pagerank_mass0",
            input=['tag://'+self.docset.ddfs_link_file_tag],
            map_reader=doclinksparse,
            map=pagerank_mass_map,
            reduce=pagerank_mass_reduce,
            sort=True,
            partitions=self.nr_partitions,
            partition=pagerank_partition,
            merge_partitions=self.merge_partitions,
            profile=self.profile,
            params=dict(iter=0, doc_count=self.docset.doc_count)))
        
    def __mass_job(self, i, results):
        return self.__run_job(self.disco.new_job(
            name="pagerank_mass%d" % i,
            input=results,
            map_reader=chain_reader,
            map=pagerank_mass_map,
            reduce=pagerank_mass_reduce,
            sort=True,
            partitions=self.nr_partitions,
            partition=pagerank_partition,
            merge_partitions=self.merge_partitions,
            profile=self.profile,
            params=dict(iter=i)))
            
    def __teleport_distribute_job(self, i, results):
        lost_mass = sum(v for k,v in result_iterator(results) \
                            if k == DANGLING_MASS_KEY)
        lost_mass_per = float(lost_mass)/self.docset.doc_count
        
        return self.__run_job(self.disco.new_job(
            name="pagerank_teleport_distribute%d" % (i-1),
            input=results,
            map_reader=chain_reader,
            map=pagerank_teleport_distribute_map,
            sort=True,
            partitions=self.nr_partitions,
            partition=pagerank_partition,
            merge_partitions=self.merge_partitions,
            profile=self.profile,
            params=dict(iter=i, alpha=self.alpha,
                        doc_count=self.docset.doc_count,
                        lost_mass_per=lost_mass_per)))
        
    def __profile_job(self, job):
        stats = job.profile_stats()
        stats.sort_stats('cumulative')
        stats.print_stats()
        
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
