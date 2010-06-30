

def pagerank_mass_map(doc, params):
    from freequery.document import Document
    
    if isinstance(doc, list) or isinstance(doc, tuple):
        doc = doc[0]

    if params['iter'] == 0:
        doc.pagerank = 1.0/params['doc_count']
        
    yield doc.uri, doc
    
    outlinks = set(doc.link_uris())
    if len(outlinks) == 0:
        out_pr = 0.0
    else:
        out_pr = doc.pagerank / len(outlinks)

    for out_uri in outlinks:
        yield out_uri, out_pr

def pagerank_teleport_map((doc,__ignore), params):
    from freequery.document import Document

    alpha = params['alpha']
    doc_count = params['doc_count']
    p = doc.pagerank
    pp = alpha*(1/doc_count) + (1-alpha)*(p)
    doc.pagerank = pp
    yield doc, 0
    
def pagerank_mass_reduce(in_iter, out, params):
    from freequery.document import Document

    doc = None
    pr = 0.0
    last_uri = None
    for uri, v in in_iter: 
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
