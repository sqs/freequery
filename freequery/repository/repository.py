import os
from freequery.repository.document_index import DocumentIndex, RepositoryPointer
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
        self.cur = RepositoryPointer(file=0, ofs=0)
        self.docindex = DocumentIndex(self.path)

        self.__open_file()

    def __path_for_file_num(self, n):
        return os.path.join(self.path, '%03d' % n)

    def __open_file(self):
        self.cur.file = 0
        filepath = self.__path_for_file_num(self.cur.file)
        if not os.path.exists(filepath):
            with open(filepath, 'w+') as f:
                f.write(" ")
        self.file = open(filepath, 'a+b')
        self.file.seek(0, os.SEEK_END)
        self.cur.ofs = self.file.tell()

    def close(self):
        self.file.close()
        self.docindex.save()
        self.docindex.close()

    def clear(self):
        for docid in self.docindex.docids():
            ptr_file = self.docindex[docid].ptr.file
            f = self.__path_for_file_num(ptr_file)
            if os.path.isfile(f):
                os.remove(f)
        self.docindex.clear()
    
    def add(self, doc):
        """
        Adds `doc` to the repository. Returns `doc`'s docid.
        """
        ptr = RepositoryPointer(0, self.cur.ofs)
        docid = self.docindex.add(doc, ptr)
        doc.docid = docid
        s = doc.pack()
        self.file.write(s)
        self.cur.ofs += len(s)
        return docid

    def get(self, docid):
        """
        Returns the `Document` with the given `docid`.
        """
        if not isinstance(docid, int):
            raise KeyError("docid must be int")
        ptr = self.docindex[docid].ptr
        return self.get_at(ptr)

    def get_at(self, ptr):
        """Returns the `Document` at the given pointer `ptr`."""
        self.file.seek(ptr.ofs, os.SEEK_SET)
        return Document.unpack_from_file(self.file)

