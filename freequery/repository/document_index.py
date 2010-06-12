import os, pickle


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
        self.entriespath = os.path.join(self.path, "entries")
        self.urimappath = os.path.join(self.path, "urimap")
        try:
            self.entriesfile = open(self.entriespath, 'r+')
            self.entries = pickle.load(self.entriesfile)
            self.urimapfile = open(self.urimappath, 'r+')
            self.urimap = pickle.load(self.urimapfile)
            self.dirty = False
        except (EOFError, IOError):
            self.entriesfile = open(self.entriespath, 'w+')
            self.entries = dict()
            self.urimapfile = open(self.urimappath, 'w+')
            self.urimap = dict()
            self.dirty = True

    def save(self):
        """
        Saves the index to disk if there are unsaved changes. Returns `True`
        if the index file was saved, and `False` otherwise.
        """
        if not self.dirty: return False
        pickle.dump(self.entries, self.entriesfile)
        pickle.dump(self.urimap, self.urimapfile)
        self.dirty = False
        return True

    def close(self):
        """Closes open files (without saving unsaved changes)."""
        self.entriesfile.close()
        self.urimapfile.close()
        self.entriesfile = None
        self.urimapfile = None

    def clear(self):
        """Erases the document index."""
        self.close()
        os.remove(self.entriespath)
        os.remove(self.urimappath)

    def __unicode__(self):
        return "<DocumentIndex path='%s' size=%d dirty=%s>" % \
               (self.path, len(self.entries), self.dirty)

    def add(self, uri, ptr):
        """
        Adds doc with `uri` to the document index, creating an entry in the URI map
        and a metadata entry with RepositoryPointer `ptr`. Fails if `uri` has
        already been added. Returns the newly created docID.
        """
        if uri in self.urimap:
            raise NotImplementedError("can't add doc with duplicate URI")
        else:
            docid = len(self.entries)
            self.urimap[uri] = docid
            self.entries[docid] = DocumentIndexEntry(ptr=ptr)
            self.dirty = True
            return docid
    
    def __len__(self):
        return len(self.entries)

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
        return self.entries[key]

    def __contains__(self, key):
        if not isinstance(key, int):
            key = self.urimap.get(key, None)
            if key is None:
                return False
        return key in self.entries

    def docids(self):
        """Returns a list of all docids."""
        return self.entries.keys()

class DocumentIndexEntry(object):

    """Stores metadata about each `Document`."""

    def __init__(self, ptr=None):
        self.ptr = ptr
    
    ptr = None
    """The `Document`'s location in a `Repository`."""

class RepositoryPointer(object):

    """Represents the location of a `Document` in a `Repository`."""

    def __init__(self, file=-1, ofs=-1):
        self.file = file
        self.ofs = ofs
    
    file = -1
    """The virtual file containing the `Document`."""
    
    ofs = -1
    """The `Document`'s offset in the virtual file."""

    def __eq__(self, other):
        return isinstance(other, RepositoryPointer) and \
               self.file == other.file and self.ofs == other.ofs

    def __str__(self):
        return "<RepositoryPointer (%d,%d)>" % (self.file, self.ofs)
