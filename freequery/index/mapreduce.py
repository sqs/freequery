"""
MapReduce functions for indexing with Discodex.
"""

TERM_SUFFIX_FOR_DOC_KEYS = ' '

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.formats.warc import WARCParser
    return WARCParser(iterable)

def doc_tfidf_map(doc, params):
    """
    For each term `t` in `doc`, emits `(t,1)` to track df (document frequency)
    and `(t, (uri,tf))` to track tf (term frequency). Appends
    `TERM_SUFFIX_FOR_DOC_KEYS` after keys tracking tf so that they sort just
    after the keys tracking df.
    """
    from freequery.index.mapreduce import TERM_SUFFIX_FOR_DOC_KEYS
    
    for t in set(doc.terms()):
        yield t.encode('utf8'), 1

    for t, tf in doc.term_frequencies().items():
        yield t.encode('utf8')+TERM_SUFFIX_FOR_DOC_KEYS, (doc.uri, tf)

def doc_tfidf_partition(key, nr_partitions, params):
    """
    Ensure that keys with or without the suffix TERM_SUFFIX_FOR_DOC_KEYS
    are sent to the same partition.
    """
    from freequery.index.mapreduce import TERM_SUFFIX_FOR_DOC_KEYS
    if key[-1] == TERM_SUFFIX_FOR_DOC_KEYS:
        key = key[:-1]
    return hash(key) % nr_partitions
        
def doc_tfidf_reduce(in_iter, out, params):
    """
    Assumes that `(t,1)`'s (to track df) are sorted before `(t,
    (uri,tf))`'s. To make this happen, keys for the latter have
    TERM_SUFFIX_FOR_DOC_KEYS appended to them.

    Emits `(t, (uri,tf-idf))`.
    """
    from freequery.index.mapreduce import TERM_SUFFIX_FOR_DOC_KEYS
    last_t = None
    done_counting_df = False
    df = 0

    for t, v in in_iter:
        if t[-1] == TERM_SUFFIX_FOR_DOC_KEYS:
            t = t[:-1] # Remove trailing TERM_SUFFIX_FOR_DOC_KEYS

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
            uri, tf = v
            idf = float(params['doc_count']) / df
            out.add(t, (uri, tf * idf))

            # We shouldn't see any more (t,1)'s for this document since the
            # (t,1)'s should be sorted before the (t,(uri,tf))'s. This makes it
            # so we don't have to hold arbitrarily long lists of (uri,tf)'s in
            # memory.
            done_counting_df = True
        else:
            raise Exception("unknown v type: %r" % v)
            
        last_t = t

def tfidf_demux((t, (uri, tfidf)), params):
    import pickle
    yield t, pickle.dumps((uri.encode('utf8'), tfidf))

def tfidf_undemux(v):
    import pickle
    uri, tfidf = pickle.loads(str(v))
    return (uri.decode('utf8'), {'tfidf': tfidf})
