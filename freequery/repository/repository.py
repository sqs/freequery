import os, pickle
from freequery.repository.document_index import DocumentIndex


class Repository(object):
    
    """
    Repository for storing `Document`s.
    """
    
    def __init__(self, path):
        """
        Creates a new `Repository` at `path`.
        """
        self.path = path
        self.docindex = DocumentIndex(os.path.join(self.path, 'docindex'))

    def close(self):
        self.docindex.close()

    def clear(self):
        for docid in self.docindex.docids():
            os.remove(self.__path_for_docid(docid))
        self.docindex.clear()

    def __path_for_docid(self, docid):
        return os.path.join(self.path, 'doc%06d' % docid)
    
    def add(self, doc):
        """
        Adds `doc` to the repository. Returns `doc`'s docid.
        """
        docid = self.docindex.add(doc.uri)
        doc.docid = docid
        docfile = open(self.__path_for_docid(docid), 'w')
        pickle.dump(doc, docfile)
        docfile.close()
        return docid

    def get(self, docid):
        """
        Returns the `Document` with the given `docid`.
        """
        if not isinstance(docid, int):
            raise KeyError("docid must be int")
        docfile = open(self.__path_for_docid(docid), 'r')
        doc = pickle.load(docfile)
        docfile.close()
        return doc
