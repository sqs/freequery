"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.repository.formats import WARCParser
    return WARCParser(iterable)

def doc_term_map(doc, params):
    """
    For each term `t` in `doc`, emits `(t,1)` to track df (document frequency)
    and `(t, (d,tf))` to track tf (term frequency).
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
    
def doc_term_reduce(in_iter, out, params):
    """
    Assumes that `(t,1)`'s (to track df) are sorted before `(t,
    (d,tf))`'s. Emits `(t, (d,tf-idf))`.
    """

def docdemux(doc, params):
    """Emits (term, docuri) for each term in `doc`."""
    tfs = ((k.encode('utf8'), v) for k,v in doc.term_frequencies().items())
    for term,tf in tfs:
        yield term, doc.uri.encode('utf8')
