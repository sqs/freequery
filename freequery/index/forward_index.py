import os, struct
from freequery.repository.document import Document
from freequery.index.forward_index_pb2 import ForwardIndexEntry as proto_ForwardIndexEntry

def term_hits_to_proto(term_hits):
    entry = proto_ForwardIndexEntry()
    for term,hits in term_hits.items():
        proto_term_hits = entry.term_hits.add()
        proto_term_hits.term = term
        for hit in hits:
            proto_hit = proto_term_hits.hits.add()
            proto_hit.pos = hit.pos
    return entry
        
class ForwardIndex(object):
    """
    Mapping of documents to term hit lists.
    """

    def __init__(self, path):
        self.path = path

        self.__open_file()

    def __open_file(self):
        open(self.path, 'a').close() # create file it doesn't exist
        self.file = open(self.path, 'a+b')

    def close(self):
        self.file.close()
        self.file = None

    def clear(self):
        self.close()
        os.remove(self.path)
        
    size_header = struct.Struct('I')
        
    def add(self, doc):
        """Add `doc` to the forward index."""
        doc.make_typed('text/html')
        entry = term_hits_to_proto(doc.term_hits())
        entry.docid = doc.docid
        s = entry.SerializeToString()
        size = entry.ByteSize()
        self.file.write(self.size_header.pack(size))
        self.file.write(s)

    def __iter__(self):
        self.file.flush()
        return ForwardIndexIterator(self.path)

class ForwardIndexIterator(object):

    def __init__(self, indexpath):
        self.file = open(indexpath, 'r')

    def next(self):
        try:
            data = self.file.read(ForwardIndex.size_header.size)
            if len(data) != ForwardIndex.size_header.size:
                raise EOFError
            size = ForwardIndex.size_header.unpack(data)[0]
        except EOFError:
            self.file.close()
            raise StopIteration
        data = self.file.read(size)
        e = proto_ForwardIndexEntry()
        e.ParseFromString(data)
        return e

    def __iter__(self):
        return self
        
