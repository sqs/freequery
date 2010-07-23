import simplejson

class ScoreDB(object):
    """ScoreDB reader."""

    def __init__(self, spec):
        if isinstance(spec, str):
            self.path = spec
        else:
            self.path = spec.scoredb_path
        self.__load()

    def __load(self):
        """Load database file into memory."""
        with open(self.path, 'rb') as dbfile:
            self.scoredict = simplejson.load(dbfile)

    def get_one(self, uri):
        """Returns the score for the document specified by `uri`."""
        return self.scoredict[uri]

    def items(self):
        return self.scoredict.items()

    def rank(self, uris=None):
        from freequery.document import Document
        # default to ranking all URIs in scoredb
        if uris is None:
            uris = self.scoredict.keys()
        # TODO(sqs): This is very inefficient as it creates a Document class to
        # wrap each item, just to perform the sort comparison (Document.__lt__).
        return [(doc.uri, doc.score) for doc in
                 sorted([Document(uri, score=score) for uri,score in self.items() \
                           if uri in uris], reverse=True)]

class ScoreDBWriter(object):

    def __init__(self, spec):
        if isinstance(spec, str):
            self.path = spec
        else:
            self.path = spec.scoredb_path
        self.dbfile = open(self.path, 'w+b')

    def set_scores(self, iterator):
        scoredict = dict(iterator)
        simplejson.dump(scoredict, self.dbfile)

    def save_and_close(self):
        self.dbfile.flush()
        self.dbfile.close()
