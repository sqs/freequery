"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.repository.formats import QTableFile
    return QTableFile(iterable)

def docdemux(doc, params):
    """Emits (term, docuri) for each term in `doc`."""
    tfs = ((k.encode('utf8'), v) for k,v in doc.term_frequencies())
    for term,tf in tfs:
        yield term, doc.uri.encode('utf8')
