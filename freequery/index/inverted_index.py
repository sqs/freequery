import os, struct, collections, copy
from freequery.index.inverted_index_pb2 import InvertedIndexEntry as proto_InvertedIndexEntry, Posting as proto_Posting
from freequery.lang.terms import prep_term

size_header = struct.Struct('I')

class InvertedIndex(object):

    def __init__(self, path):
        """
        Opens an inverted index at `path`.
        """
        self.path = path

    def close(self):
        """Closes the index file."""
        self.file.close()
        self.file = None
    
    def __unicode__(self):
        return "<%s path='%s'>" % (self.__class__.__name__, self.path)

    __str__ = __unicode__
    __repr__ = __unicode__

    
class InvertedIndexReader(InvertedIndex):

    """
    Reads and queries an inverted index.
    """

    def __init__(self, path):
        super(InvertedIndexReader, self).__init__(path)
        self.__open_file()

    def __open_file(self):
        self.file = open(self.path, 'rb')

    def __iter__(self):
        return InvertedIndexIterator(self.path)
        
    def lookup(self, token):
        """Returns a list of postings for `Document`s that contain `token`."""
        term = prep_term(token)
        for e in self.__iter__():
            if e.term == term:
                return e.postings
        return []

class InvertedIndexIterator(object):

    def __init__(self, path):
        self.file = open(path, 'rb')

    def next(self):
        try:
            data = self.file.read(size_header.size)
            if len(data) != size_header.size:
                raise EOFError
            size = size_header.unpack(data)[0]
        except EOFError:
            self.file.close()
            raise StopIteration
        data = self.file.read(size)
        e = proto_InvertedIndexEntry()
        e.ParseFromString(data)
        return e

    def __iter__(self):
        return self


class InvertedIndexWriter(InvertedIndex):

    """
    Writes an inverted index.
    """

    def __init__(self, path):
        super(InvertedIndexWriter, self).__init__(path)
        self.__open_file()
    
    def __open_file(self):
        self.file = open(self.path, 'w+b')
        self.postings = collections.defaultdict(list)
        self.saved = False

    def clear(self):
        """Removes the index file."""
        self.close()
        os.remove(self.path)
        
    def add(self, e):
        """Adds a `ForwardIndexEntry` `e` to the inverted index in memory."""
        if self.saved:
            raise NotImplementedError("can't add to index after saving")
        docid = e.docid
        term_hits = e.term_hits
        for th in term_hits:
            posting = proto_Posting()
            posting.docid = docid
            for th_hit in th.hits:
                h = posting.hits.add()
                h.CopyFrom(th_hit)
            self.postings[th.term].append(posting)
    
    def save(self):
        terms = self.postings.keys()
        terms.sort()

        entry = proto_InvertedIndexEntry()

        for term in terms:
            entry.term = term
            for posting in self.postings[term]:
                proto_posting = entry.postings.add()
                proto_posting.CopyFrom(posting)
            s = entry.SerializeToString()
            size = entry.ByteSize()
            self.file.write(size_header.pack(size))
            self.file.write(s)
            entry.Clear()
        self.file.flush()
