import discodb
from discodex.client import DiscodexClient
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
        self.spec = Spec(spec)
        self.discodex_client = DiscodexClient()

    def query(self, q):
        """Return list `Document` instances matching query `q`, without ranking."""
        qq = discodb.Q.parse(q)
        return (Document(uri, "TODO") for uri in
                self.discodex_client.query(self.spec.invindex_name, qq))

    def search(self, q):
        pass
