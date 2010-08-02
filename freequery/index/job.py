from disco.core import Disco, result_iterator
from disco.settings import DiscoSettings
from disco.func import chain_reader
from discodex.objects import DataSet
from freequery.document import docparse
from freequery.document.docset import Docset
from freequery.index.tf_idf import TfIdf


class IndexJob(object):

    def __init__(self, spec, discodex,
                 disco_addr="disco://localhost", profile=False):
        # TODO(sqs): refactoring potential with PagerankJob
        self.spec = spec
        self.discodex = discodex
        self.docset = Docset(spec.docset_name)
        self.disco = Disco(DiscoSettings()['DISCO_MASTER'])
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
            map=TfIdf.map,
            reduce=TfIdf.reduce,
            sort=True,
            partitions=self.nr_partitions,
            partition=TfIdf.partition,
            merge_partitions=False,
            profile=self.profile,
            params=dict(doc_count=self.docset.doc_count))

    def __run_discodex_index(self, results):
        opts = {
            'parser': 'disco.func.chain_reader',
            'demuxer': 'freequery.index.tf_idf.TfIdf_demux',
            'nr_ichunks': 1, # TODO(sqs): after disco#181 fixed, increase this
        }
        ds = DataSet(input=results, options=opts)
        origname = self.discodex.index(ds)
        self.disco.wait(origname) # origname is also the disco job name
        self.discodex.clone(origname, self.spec.invindex_name)
        
