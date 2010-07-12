'''
Pagerank MapReduce functions
============================

Notation
--------
:math:`n` : number of documents.

:math:`\\alpha \\in (0,1]` : parameter; a random surfer will teleport to a random
page with probability :math:`(1-\\alpha)`.

:math:`P(i)` : pagerank of node :math:`i`.

:math:`C(i)` : number of outgoing links in node :math:`i`.
'''

DANGLING_MASS_KEY = '::dangling_node::'

def pagerank_mass_map(doc, params):
    """
    Passes node :math:`i`'s pagerank along its outgoing links.

    On the first iteration, initializes :math:`P(i) := 1/n`. 

    For each of :math:`i`'s outgoing links, emits
    :math:`\\left( \\mathrm{out\_uri}, P(i)/C(i) \\right)`.
    """
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
        
    yield doc.uri.encode('utf8'), doc

    assert doc._Document__cached_link_uris is not None
    outlinks = doc.link_uris
    if len(outlinks) > 0:
        out_pr = doc.pagerank / len(outlinks)
        for out_uri in outlinks:
            yield out_uri.encode('utf8'), out_pr
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


def pagerank_partition(key, nr_partitions, params):
    from freequery.document import Document
    if isinstance(key, Document):
        doc = key
        return hash(doc.uri) % nr_partitions
    elif isinstance(key, unicode) or isinstance(key, str):
        return hash(key) % nr_partitions
    else:
        raise Exception("unknown key type: %r" % key)
    
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
 
