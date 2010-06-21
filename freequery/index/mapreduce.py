"""
MapReduce functions for indexing with Discodex.
"""

def docparse(iterable, size, fname, params):
    """Iterates through a Web dump. For each page, strips HTML
    and other control data and uses each stemmed term as a key for the value ``uri`` of the page.
    """
    from freequery.repository.formats import QTableFile
    for doc in QTableFile(iterable):
        for word in set(doc.terms()):
            yield word, doc.uri
