import os, pickle


class DocumentIndex(object):

    """
    Maintains a uri->docID mapping for `Repository`.
    """

    def __init__(self, indexpath):
        """
        Opens a document index file at `indexfile`, creating it if it doesn't
        exist.
        """
        self.indexpath = indexpath
        try:
            self.indexfile = open(self.indexpath, 'r+')
            self.index = pickle.load(self.indexfile)
            self.dirty = False
        except IOError, EOFError:
            self.indexfile = open(self.indexpath, 'w+')
            self.index = dict()
            self.dirty = True

    def save(self):
        """
        Saves the index to disk if there are unsaved changes. Returns `True`
        if the index file was saved, and `False` otherwise.
        """
        if not self.dirty: return False
        pickle.dump(self.index, self.indexfile)
        self.dirty = False
        return True

    def close(self):
        """Closes the index file (and saves it if there are unsaved changes)."""
        self.save()
        if self.indexfile:
            self.indexfile.close()

    def clear(self):
        """Removes the index file."""
        if self.indexfile:
            self.indexfile.close()
        os.remove(self.indexpath)

    def __unicode__(self):
        return "<DocumentIndex path='%s' size=%d dirty=%s>" % \
               (self.indexpath, len(self.index), self.dirty)

    def add(self, uri):
        """
        If `uri` is not in the index, create and return a new docID for it;
        otherwise, return its existing docID.
        """
        if uri in self.index:
            return self.index[uri]
        else:
            docid = len(self.index)
            self.index[uri] = docid
            self.dirty = True
            return docid
    
    def __len__(self):
        return len(self.index)

    def __getitem__(self, uri):
        return self.index[uri]

    def __contains__(self, uri):
        return uri in self.index

    def docids(self):
        """Returns a list of all docids."""
        return self.index.values()
