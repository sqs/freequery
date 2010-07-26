from freequery.formats.warc import WARCWriter
from freequery.document import Document

class QTableFile(object):

    """Parser for QTable dump files."""

    DELIM = "@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@\n"
    
    def __init__(self, iterable):
        self.pos = 0
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

    def tell(self):
        """Returns the cursor position (in bytes) in `iterable`. Used for the
        :class:`Docset` index."""
        return self.pos
            
    def next(self):
        if self.iterable is None:
            raise Exception("iterable shouldn't be none")
        
        # URI
        uri = self.iterable.next()
        self.pos += len(uri)
        uri = uri.strip().decode('utf8')

        # meta
        # ignoring for now
        for line in self.iterable:
            self.pos += len(line)
            if line == "\n":
                break

        # raw
        raw = []
        for line in self.iterable:
            self.pos += len(line)
            if line == self.DELIM:
                break # doc finished
            else:
                raw.append(line.decode('utf8'))

        # remove "\n" from last line of raw, since it delimits
        # the raw from the end-of-document and is not actually part
        # of the raw content
        if len(raw) > 0:
            raw[-1] = raw[-1].rstrip()
            
        return Document(uri, u''.join(raw))

    def __iter__(self):
        return self

import sys
inpath = sys.argv[1]
outpath = inpath + '.warc'
infile = open(inpath, 'rb')
outfile = open(outpath, 'w+b')
warcwriter = WARCWriter(outfile)

for doc in QTableFile(infile):
    warcwriter.write(doc)
