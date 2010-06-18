"""
Parsers for various formats of Web page dumps.
"""
from freequery.document import Document


class QTableFile(object):

    """Parser for QTable dump files."""

    DELIM = "@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@\n"
    
    def __init__(self, iterable):
        self.iterable = iterable.__iter__()

    def next(self):
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
            if line != self.DELIM:
                raw.append(line)
            else: # doc finished
                break
        return Document(uri, ''.join(raw))

    def __iter__(self):
        pass
