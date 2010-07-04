"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.repository.formats import QTableFile
    return QTableFile(iterable)

def docdemux(doc, params):
    """For each document, strips HTML and other control data from the
    content... TODO. The following is not currently true: and emits `(uri,
    tf)`, where `tf` is the term frequency in this document (uses in-mapper
    combining to calculate these here)."""
    str_terms = (str(t.decode('utf8')) for t in doc.terms())
    for term in set(str_terms):
        yield term, doc.uri
