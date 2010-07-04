import discodb
from disco.util import urlresolve
from discodex.client import DiscodexClient
from discodex.objects import DataSet
from freequery.repository.docset import Docset
from freequery.document import Document

class Spec(object):
    docset_prefix = 'fq:docset:'
    
    def __init__(self, name):
        if isinstance(name, Spec):
            raise "Spec(name) expects string name, not Spec name"
        self.name = name
        self.docset_name = '%s%s' % (self.docset_prefix, name)
        self.invindex_name = 'discodex:fq:%s:invindex' % name
        self.scoredb_path = '/tmp/fq-scoredb'

class FreequeryClient(object):

    def __init__(self, spec):
        if isinstance(spec, Spec):
            self.spec = spec
        else:
            self.spec = Spec(spec)
        self.discodex_client = DiscodexClient()

    def query(self, q):
        """Return list `Document` instances matching query `q`, without ranking."""
        qq = discodb.Q.parse(q)
        return (Document(uri, "TODO") for uri in
                self.discodex_client.query(self.spec.invindex_name, qq))

    def search(self, q):
        pass

    def index(self):
        import sys, time
        
        docset = Docset(self.spec.docset_name)
        if not docset.exists():
            print "fq: cannot index `%s': no such docset" % self.spec.docset_name
            exit(1)

        dataset = DataSet(input=map(urlresolve, list(docset.dump_uris())),
                          options=dict(parser='freequery.index.mapreduce.docparse',
                                       demuxer='freequery.index.mapreduce.docdemux',
                                       ))
        orig_invindex_name = self.discodex_client.index(dataset)
        if orig_invindex_name:
            print "indexing: %s " % orig_invindex_name,
        else:
            print "fq: discodex failed to index `%s'" % self.spec.name
            exit(2)
        
        # wait for indexing to complete
        while True:
            try:
                self.discodex_client.get(orig_invindex_name)
                break
            except:
                time.sleep(2)
                sys.stdout.write(".")
                sys.stdout.flush()
        self.discodex_client.clone(orig_invindex_name, self.spec.invindex_name)
