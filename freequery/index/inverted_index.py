import os, cPickle as pickle, copy

class InvertedIndex(object):

    """
    Inverted index of terms to documents.
    """

    def __init__(self, path):
        """
        Opens an inverted index file at `path`, creating it if it doesn't
        exist.
        """
        self.path = path
        try:
            self.file = open(self.path, 'r+')
            self.term_doclists = pickle.load(self.file)
            self.new = False
        except IOError, EOFError:
            self.file = open(self.path, 'w+')
            self.term_doclists = dict()
            self.new = True

    def save(self):
        """
        Saves the index to disk.
        """
        if not self.new:
            raise NotImplementedError("can't update an existing index")
        pickle.dump(self.term_doclists, self.file)
        self.new = False
        return True

    def close(self):
        """Closes the index file."""
        if self.file:
            self.file.close()
            self.file = None

    def clear(self):
        """Removes the index file."""
        if self.file:
            self.file.close()
        os.remove(self.path)

    def __unicode__(self):
        return "<InvertedIndex path='%s' size=%d new=%s>" % \
           (self.path, len(self.index), self.new)

    def add(self, docs):
        """Adds a list of `Document`s to the inverted index."""
        if not self.new:
            raise NotImplementedError("can't add to existing index")
        for doc in docs:
            term_hits = doc.term_hits()
            for term,hits in term_hits.items():
                if term not in self.term_doclists:
                    self.term_doclists[term] = dict()
                self.term_doclists[term][doc.docid] = hits

    def merge(self, invindex1, invindex2):
        """
        Merges two other `InvertedIndex`es together into this one. The two
        indexes must not share any documents.
        """
        if not self.new:
            raise NotImplementedError("can't merge into existing index")
        self.term_doclists = copy.deepcopy(invindex1.term_doclists)
        term_doclists2 = copy.deepcopy(invindex2.term_doclists)
        for term,doclist in term_doclists2.items():
            if term in self.term_doclists:
                self.term_doclists[term].update(doclist)
            else:
                self.term_doclists[term] = doclist
        

    def lookup(self, term):
        """Returns a list of docids of `Document`s that contain `term`."""
        return self.term_doclists.get(term, {})
