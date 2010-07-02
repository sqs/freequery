DANGLING_MASS_KEY = '::dangling_node::'

def pagerank_mass_map(doc, params):
    from freequery.document import Document
    from freequery.graph.pagerank import DANGLING_MASS_KEY

    # The first iteration gets just plain Document instances,
    # but subsequent iterations actually see the `(doc, 0)`
    # data emitted by pagerank_teleport_distribute_map. Just
    # collapse these--ignore the 0.
    if isinstance(doc, list) or isinstance(doc, tuple):
        doc = doc[0]
    
    if params['iter'] == 0:
        doc.pagerank = 1.0/params['doc_count']
        
    yield doc.uri, doc
    
    outlinks = set(doc.link_uris())
    if len(outlinks) > 0:
        out_pr = doc.pagerank / len(outlinks)
        for out_uri in outlinks:
            if isinstance(out_uri, unicode):
                out_uri = out_uri.encode('utf8')
            yield out_uri, out_pr
    else:
        # This is a dangling node. We will sum the
        # pageranks of all dangling nodes and redistribute
        # it proportionally to all other nodes in a later
        # job.
        yield DANGLING_MASS_KEY, doc.pagerank

def pagerank_teleport_distribute_map((doc,__ignore), params):
    from freequery.document import Document
    from freequery.graph.pagerank import DANGLING_MASS_KEY
    
    # Ignore the dangling mass count. It's an artifact from
    # the previous job and is already reflected in
    # params['lost_mass_per'].
    if doc == DANGLING_MASS_KEY:
        return
    
    alpha = params['alpha']
    doc_count = params['doc_count']
    lost_mass_per = params['lost_mass_per']
    p = doc.pagerank
    pp = alpha*(1.0/doc_count) + (1-alpha)*(lost_mass_per+p)
    doc.pagerank = pp
    yield doc, 0
    
def pagerank_mass_reduce(in_iter, out, params):
    from freequery.document import Document
    from freequery.graph.pagerank import DANGLING_MASS_KEY

    doc = None
    pr = 0.0
    dangling_mass = 0.0
    last_uri = None
    for uri, v in in_iter:
        # msg("(uri,v) = (%r, %r)" % (uri,v))
        
        if uri == DANGLING_MASS_KEY:
            dangling_mass += v
            continue
        
        if uri != last_uri:
            if doc:
                doc.pagerank = pr
                out.add(doc, 0)
                doc = None
            else:
                # If this pr value were for a document in the docset,
                # then (because the input is sorted) `doc` would be set
                # here. Since it's not, this is a dangling node.
                out.add(DANGLING_MASS_KEY, pr)
            pr = 0.0
                
        if isinstance(v, Document):
            doc = v
        elif isinstance(v, float):
            pr += v
        else:
            raise Exception("unknown v type: %r" % v)
        last_uri = uri
        
    # emit last doc
    if doc:
        doc.pagerank = pr
        out.add(doc, 0)
    else:
        # See explanation in the `for`-loop above about why we know this is a
        # dangling node.
        out.add(DANGLING_MASS_KEY, pr)

    # emit dangling mass
    out.add(DANGLING_MASS_KEY, dangling_mass)

class PagerankJob(object):

    def __init__(self, docset, disco_addr="disco://localhost",
                 alpha=0.15, niter=3):
        from disco.core import Disco
        self.docset = docset
        self.disco = Disco("disco://localhost")
        self.alpha = alpha
        self.niter = niter
        self.doc_count = 184 # TODO: don't hardcode

    def start(self):
        from disco.core import result_iterator
        from disco.func import chain_reader
        from freequery.index.mapreduce import docparse
        from freequery.graph.pagerank import pagerank_mass_map, \
            pagerank_mass_reduce, pagerank_teleport_distribute_map

        results = self.disco.new_job(
            name="pagerank_mass0",
            input=self.docset.dump_uris(),
            map_reader=docparse,
            map=pagerank_mass_map,
            reduce=pagerank_mass_reduce,
            sort=True,
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
                params=dict(iter=i)).wait()

        # write scoredb
        from freequery.graph.scoredb import ScoreDBWriter
        from freequery.document import Document
        db = ScoreDBWriter('/s/a/scoredb') # TODO: don't hardcode
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
