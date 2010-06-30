"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump and emits each document."""    
    from freequery.repository.formats import QTableFile
    for doc in QTableFile(iterable):
        yield doc

def docdemux(doc, params):
    """For each document, strips HTML and other control data from the
    content and emits `(uri, tf)`, where `tf` is the term frequency in
    this document (uses in-mapper combining to calculate these here)."""
    for term,tf in doc.term_frequencies().items():
        yield term, doc.uri

