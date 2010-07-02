"""
Parsers for various formats of Web page dumps.
"""
from freequery.document import Document


class QTableFile(object):

    """Parser for QTable dump files."""

    DELIM = "@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@\n"
    
    def __init__(self, iterable):
        if isinstance(iterable, file):
            self.iterable = iterable.__iter__()
        elif hasattr(iterable, 'read'):
            # disco.comm.Connection objects are iterator-like, but they don't
            # define __iter__ or next(), so just read in the whole
            # buffer. TODO: submit a patch to disco to have Connection expose
            # an iterator interface.
            self.iterable = iter(iterable.read().splitlines(True))
        elif isinstance(iterable, list):
            self.iterable = iter(iterable)

    def next(self):
        if self.iterable is None:
            raise Exception("iterable shouldn't be none")
        
        # URI
        uri = self.iterable.next().strip()

        # meta
        # ignoring for now
        for line in self.iterable:
            if line == "\n":
                break

        # raw
        raw = []
        for line in self.iterable:
            if line == self.DELIM:
                break # doc finished
            else:
                raw.append(line)

        # remove "\n" from last line of raw, since it delimits
        # the raw from the end-of-document and is not actually part
        # of the raw content
        if len(raw) > 0:
            raw[-1] = raw[-1].rstrip()
            
        return Document(uri, ''.join(raw))

    def __iter__(self):
        return self

class QTableFileWriter(object):

    """Writer for QTable dump files."""
    
    def __init__(self, out):
        self.out = out

    def write(self, doc):
        """Writes `doc` to the output stream."""
        self.out.writelines((doc.uri, "\n\n", doc.raw, "\n", QTableFile.DELIM))

    
