"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.repository.formats import WARCParser
    return WARCParser(iterable)

def doc_tfidf_map(doc, params):
    """
    For each term `t` in `doc`, emits `(t,1)` to track df (document frequency)
    and `(t, (doc,tf))` to track tf (term frequency).
    """
    for t in set(doc.terms()):
        yield t, 1

    for t, tf in doc.term_frequencies().items():
        yield t, (doc, tf)

#def doc_term_partition(key, nr_partitions, params):
#    """
#    Ensures entries with the same key (term) are partitioned together.
#    """
#    return hash(key) % nr_partitions
    
def doc_tfidf_reduce(in_iter, out, params):
    """
    Assumes that `(t,1)`'s (to track df) are sorted before `(t,
    (doc,tf))`'s. Emits `(t, (doc,tf-idf))`.
    """
    last_t = None
    done_counting_df = False
    df = 0

    for t, v in in_iter:
        if t != last_t:
            # Then we're done with this term.
            done_counting_df = False
            df = 0
            assert isinstance(v, int) # (t,1)'s should come first
            
        if isinstance(v, int):
            if done_counting_df:
                raise Exception("done_counting_df=True but encountered df " \
                                "value for term '%s'" % t)
            df += v
        elif isinstance(v, tuple) or isinstance(v, list):
            doc, tf = v
            idf = float(params['doc_count']) / df
            out.add(t, (doc, tf * idf))

            # We shouldn't see any more (t,1)'s for this document since the
            # (t,1)'s should be sorted before the (t,(doc,tf))'s. This makes it
            # so we don't have to hold arbitrarily long lists of (doc,tf)'s in
            # memory.
            done_counting_df = True
            
        last_t = t
            

def docdemux(doc, params):
    """Emits (term, docuri) for each term in `doc`."""
    tfs = ((k.encode('utf8'), v) for k,v in doc.term_frequencies().items())
    for term,tf in tfs:
        yield term, doc.uri.encode('utf8')
