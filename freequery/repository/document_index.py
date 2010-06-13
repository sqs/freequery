import os, cPickle as pickle
from freequery.repository.repository_pb2 import DocumentIndex as proto_DocumentIndex
proto_DocumentIndexEntry = proto_DocumentIndex.DocumentIndexEntry


class DocumentIndex(object):

    """
    Stores document metadata and contains a uri->docID mapping for `Repository`.
    """

    def __init__(self, path):
        """
        Opens a document index file at `path`, creating it if it doesn't
        exist.
        """
        self.path = path
        self.docindexpath = os.path.join(self.path, "docindex")
        self.urimappath = os.path.join(self.path, "urimap")
        self.dirty = False
        
        self.__open_files()
        
    def __open_files(self):
        # create files if they don't exist
        if not os.path.isfile(self.docindexpath):
            open(self.docindexpath, 'a').close()
        if not os.path.isfile(self.urimappath):
            open(self.urimappath, 'a').close()

        self.docindexfile = open(self.docindexpath, 'r+')
        self.docindex = proto_DocumentIndex()
        self.docindex.ParseFromString(self.docindexfile.read())
        
        self.urimapfile = open(self.urimappath, 'r+')
        try:
            self.urimap = pickle.load(self.urimapfile)
        except EOFError:
            self.urimap = dict()
        
    def save(self):
        """
        Saves the index to disk if there are unsaved changes. Returns `True`
        if the index file was saved, and `False` otherwise.
        """
        if not self.dirty: return False

        s = self.docindex.SerializeToString()
        self.docindexfile.seek(0)
        self.docindexfile.write(s)
        
        pickle.dump(self.urimap, self.urimapfile)

        self.dirty = False
        return True

    def close(self):
        """Closes open files (without saving unsaved changes)."""
        self.docindexfile.close()
        self.urimapfile.close()
        self.docindexfile = None
        self.urimapfile = None

    def clear(self):
        """Erases the document index."""
        self.dirty = True
        self.close()
        os.remove(self.docindexpath)
        os.remove(self.urimappath)

    def __unicode__(self):
        return "<DocumentIndex path='%s' size=%d dirty=%s>" % \
               (self.path, len(self.docindex), self.dirty)

    def add(self, uri, ptr):
        """
        Adds doc with `uri` to the document index, creating an entry in the URI map
        and a metadata entry with RepositoryPointer `ptr`. Fails if `uri` has
        already been added. Returns the newly created docID.
        """
        assert isinstance(uri, str) or isinstance(uri, unicode)
        if uri in self.urimap:
            raise NotImplementedError("can't add doc with duplicate URI")
        else:
            docid = len(self.docindex.entries)
            self.urimap[uri] = docid

            entry = self.docindex.entries.add()
            entry.docid = docid
            entry.uri = uri.decode('utf8')
            entry.ptr_file = ptr.file
            entry.ptr_ofs = ptr.ofs

            self.dirty = True
            return docid
    
    def __len__(self):
        return len(self.docindex.entries)

    def __key_to_docid(self, key):
        """
        Given either a URI or docID, return the docID itself or the docID
        corresponding to the URI.
        """
        if isinstance(key, int):
            return key
        else:
            return self.urimap[key]
    
    def __getitem__(self, key):
        if not isinstance(key, int):
            key = self.urimap.get(key, None)
            if key is None:
                raise KeyError("URI not found in urimap")
        for e in self.docindex.entries:
            if e.docid == key:
                return e
        raise KeyError("docid %d not found in doc index" % key)

    def __contains__(self, key):
        if not isinstance(key, int):
            key = self.urimap.get(key, None)
            if key is None:
                return False
        return key in self.docids()

    def docids(self):
        """Returns a list of all docids."""
        return [e.docid for e in self.docindex.entries]

class rptr(object):
    file = -1
    ofs = -1

    def __init__(self, file, ofs):
        self.file = file
        self.ofs = ofs

    def __eq__(self, other):
        return self.file == other.file and self.ofs == other.ofs
