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
            yield out_uri, out_pr
    else:
        # This is a dangling node. We will sum the
        # pageranks of all dangling nodes and redistribute
        # it proportionally to all other nodes in a later
        # job.
        print "!!!!!!!!!!!!!! doc=%r pr=%f" % (doc,doc.pagerank)
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
        if uri == DANGLING_MASS_KEY:
            dangling_mass += v
            continue
        
        if doc and uri != last_uri:
            doc.pagerank = pr
            out.add(doc, 0)
            doc = None
            pr = 0.0

        if isinstance(v, Document):
            doc = v
        elif isinstance(v, float):
            pr += v
        else:
            raise Exception("unknown v type: %r" % v)
        last_uri = uri
        
    # emit last doc
    doc.pagerank = pr
    out.add(doc, 0)

    # emit dangling mass
    out.add(DANGLING_MASS_KEY, dangling_mass)
