import os, struct, cPickle as pickle
from freequery.repository.repository_pb2 import DocumentIndexEntry as proto_DocumentIndexEntry


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
        self.urimap_dirty = False
        
        self.__open_files()
        
    def __open_files(self):
        # create files if they don't exist
        if not os.path.isfile(self.docindexpath):
            open(self.docindexpath, 'a').close()
        if not os.path.isfile(self.urimappath):
            open(self.urimappath, 'a').close()

        self.docindexfile = open(self.docindexpath, 'a+b')
        
        self.urimapfile = open(self.urimappath, 'r+')
        try:
            self.urimap = pickle.load(self.urimapfile)
        except EOFError:
            self.urimap = dict()

    size_header = struct.Struct('I')
            
    def save(self):
        """
        Saves the URI map to disk if there are unsaved changes. Returns `True`
        if the URI map file was saved, and `False` otherwise. The docindex file
        is continuously written and does not need to be explicitly saved.
        """
        if not self.urimap_dirty: return False
        pickle.dump(self.urimap, self.urimapfile)
        self.urimap_dirty = False
        return True

    def close(self):
        """Closes open files (without saving unsaved changes)."""
        self.docindexfile.close()
        self.urimapfile.close()
        self.docindexfile = None
        self.urimapfile = None

    def clear(self):
        """Erases the document index."""
        self.urimap_dirty = True
        self.close()
        os.remove(self.docindexpath)
        os.remove(self.urimappath)

    def __unicode__(self):
        return "<DocumentIndex path='%s' size=%d dirty=%s>" % \
               (self.path, len(self.docindex), self.urimap_dirty)

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
            docid = len(self.urimap)
            self.urimap[uri] = docid
            self.urimap_dirty = True

            entry = proto_DocumentIndexEntry()
            entry.docid = docid
            entry.uri = uri.decode('utf8')
            entry.ptr_file = ptr.file
            entry.ptr_ofs = ptr.ofs
            s = entry.SerializeToString()
            size = entry.ByteSize()
            self.docindexfile.write(self.size_header.pack(size))
            self.docindexfile.write(s)

            return docid
    
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
        for e in self.__iter__():
            if e.docid == key:
                return e
        raise KeyError("docid %d not found in doc index" % key)

    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __iter__(self):
        self.docindexfile.flush()
        return DocumentIndexIterator(self.docindexpath)

class DocumentIndexIterator(object):

    def __init__(self, path):
        self.file = open(path, 'r')

    def next(self):
        try:
            data = self.file.read(DocumentIndex.size_header.size)
            if len(data) != DocumentIndex.size_header.size:
                raise EOFError
            size = DocumentIndex.size_header.unpack(data)[0]
        except EOFError:
            self.file.close()
            raise StopIteration
        data = self.file.read(size)
        e = proto_DocumentIndexEntry()
        e.ParseFromString(data)
        return e

    def __iter__(self):
        return self
    
class rptr(object):
    file = -1
    ofs = -1

    def __init__(self, file, ofs):
        self.file = file
        self.ofs = ofs

    def __eq__(self, other):
        return self.file == other.file and self.ofs == other.ofs

    def __str__(self):
        return "rptr(%d,%d)" % (self.file, self.ofs)

    __unicode__ = __str__
    __repr__ = __str__
