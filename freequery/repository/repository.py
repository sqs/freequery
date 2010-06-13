import os
from freequery.repository.document_index import DocumentIndex, rptr
from freequery.repository.document import Document


class Repository(object):
    
    """
    Repository for storing `Document`s.
    """
    
    def __init__(self, path):
        """
        Opens a repository at `path`, creating it if needed.
        """
        self.path = path
        self.cur = rptr(-1,-1)
        self.docindex = DocumentIndex(self.path)

        self.__open_file()

    def __path_for_file_num(self, n):
        return os.path.join(self.path, '%03d' % n)

    def __open_file(self):
        self.cur.file = 0
        filepath = self.__path_for_file_num(self.cur.file)
        if not os.path.exists(filepath):
            open(filepath, 'a').close() # create if doesn't exist
        self.file = open(filepath, 'a+b')
        self.cur.ofs = self.file.tell()

    def close(self):
        self.file.close()
        self.docindex.save()
        self.docindex.close()

    def clear(self):
        for docid in self.docindex.docids():
            ptr_file = self.docindex[docid].ptr_file
            f = self.__path_for_file_num(ptr_file)
            if os.path.isfile(f):
                os.remove(f)
        self.docindex.clear()
    
    def add(self, doc):
        """
        Adds `doc` to the repository. Returns `doc`'s docid.
        """
        docid = self.docindex.add(doc.uri, self.cur)
        doc.docid = docid
        s = doc.to_proto_string()
        self.file.write(s)
        self.cur.ofs += len(s)
        return docid

    def get(self, docid):
        """
        Returns the `Document` with the given `docid`.
        """
        if not isinstance(docid, int):
            raise KeyError("docid must be int")
        entry = self.docindex[docid]
        ptr = rptr(entry.ptr_file, entry.ptr_ofs)
        return self.get_at(ptr)

    def get_at(self, ptr):
        """Returns the `Document` at the given pointer `ptr`."""
        self.file.seek(ptr.ofs, os.SEEK_SET)
        return Document.from_proto_file(self.file)

    def __iter__(self):
        """Iterator over all documents stored in this repository."""
        self.file.flush()
        return RepositoryIterator(self.__path_for_file_num(self.cur.file))

class RepositoryIterator(object):

    def __init__(self, path):
        self.file = open(path, 'rb')
        
    def next(self):
        try:
            return Document.from_proto_file(self.file)
        except EOFError:
            self.file.close()
            raise StopIteration
    
    def __iter__(self):
        return self

