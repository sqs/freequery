from disco.core import Disco, result_iterator
from disco.func import chain_reader
from discodex.objects import DataSet
from freequery.repository.docset import Docset
from freequery.index.mapreduce import \
    docparse, doc_tfidf_map, doc_tfidf_partition, doc_tfidf_reduce


class IndexJob(object):

    def __init__(self, spec, discodex,
                 disco_addr="disco://localhost", profile=False):
        # TODO(sqs): refactoring potential with PagerankJob
        self.spec = spec
        self.discodex = discodex
        self.docset = Docset(spec.docset_name)
        self.disco = Disco("disco://localhost")
        self.nr_partitions = 8
        self.profile = profile

    def start(self):
        results = self.__run_job(self.__index_job())
        self.__run_discodex_index(results)

    def __run_job(self, job):
        results = job.wait()
        if self.profile:
            self.__profile_job(job)
        return results
        
    def __index_job(self):
        return self.disco.new_job(
            name="index_tfidf",
            input=['tag://' + self.docset.ddfs_tag],
            map_reader=docparse,
            map=doc_tfidf_map,
            reduce=doc_tfidf_reduce,
            sort=True,
            partitions=self.nr_partitions,
            partition=doc_tfidf_partition,
            merge_partitions=False,
            profile=self.profile,
            params=dict(doc_count=self.docset.doc_count))

    def __run_discodex_index(self, results):
        dataset = DataSet(input=results,
                          options=dict(parser='discodex.mapreduce.parsers.netstrparse',
                                       demuxer='freequery.index.mapreduce.tfidf_demux'))
        orig_invindex_name = self.discodex.index(dataset)
        if not orig_invindex_name:
            raise Exception("fq: discodex failed to index `%s'" % self.spec.name)

        # wait for indexing to complete
        while True:
            try:
                self.discodex.get(orig_invindex_name)
                self.discodex.clone(orig_invindex_name, self.spec.invindex_name)
                break
            except Exception as e:
                import time
                # TODO(sqs): find a better way of monitoring job status
                print "."
                print e
                time.sleep(2)



