import discodb
from discodex.client import DiscodexClient
from freequery.document import Document

class FreequeryClient(object):

    def __init__(self, spec):
        self.spec = spec
        self.discodex_client = DiscodexClient()

    def query(self, q):
        """Return list `Document` instances matching query `q`, without ranking."""
        qq = discodb.Q.parse(q)
        return (Document(uri, "TODO") for uri in
                self.discodex_client.query(self.spec, qq))
