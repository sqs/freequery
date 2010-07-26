from disco.util import urlresolve
from discodex.client import DiscodexClient
from freequery.repository.docset import Docset
from freequery.document import Document
from freequery.document.score import Score
from freequery.graph.pagerank_job import PagerankJob
from freequery.graph.links import LinkParseJob
from freequery.index.job import IndexJob
from freequery.index.scoredb import ScoreDB
from freequery.index.mapreduce import tfidf_undemux
from freequery.query import Query


class Spec(object):
    docset_prefix = 'fq:docset:'
    
    def __init__(self, name):
        if isinstance(name, Spec):
            raise "Spec(name) expects string name, not Spec name"
        self.name = name
        self.docset_name = '%s%s' % (self.docset_prefix, name)
        self.invindex_name = 'discodex:fq:%s:invindex' % name
        self.scoredb_path = '/s/a/scoredb-%s' % name

class FreequeryClient(object):

    def __init__(self, spec):
        if isinstance(spec, Spec):
            self.spec = spec
        else:
            self.spec = Spec(spec)
        self.discodex_client = DiscodexClient()
        self.docset = Docset(self.spec.docset_name)

    def query(self, q, ranked=True):
        """Return a ranked list of matching `Document` instances."""
        qq = Query.parse(q)
        res = self.discodex_client.query(self.spec.invindex_name, qq)
        res = map(tfidf_undemux, res)
        if not res:
            return []

        pageranks = None
        if ranked:
            scoredb = ScoreDB(self.spec.scoredb_path)
            uris = [e[0] for e in res]
            pageranks = dict(scoredb.rank(uris))
            if not pageranks:
                raise Exception("no ranks available")
            
        docs = []
        for uri,scores in res:
            doc = self.docset.get(uri)
            doc.score = Score(**scores)
            if pageranks:
                doc.score['pagerank'] = pageranks[uri]
            doc.excerpt = doc.excerpt(qq)
            docs.append(doc)
        return docs

    def index(self, **kwargs):
        if not self.docset.exists():
            print "fq: cannot index `%s': no such docset" % self.spec.docset_name
            exit(1)
        job = IndexJob(self.spec, self.discodex_client, **kwargs)
        job.start()


    def linkparse(self, **kwargs):
        job = LinkParseJob(self.spec, **kwargs)
        job.start()
        
    def rank(self, **kwargs):
         job = PagerankJob(self.spec, **kwargs)
         job.start()
