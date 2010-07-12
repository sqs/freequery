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

    def ranked_uris(self, uris=None):
        # default to ranking all URIs
        if uris is None:
            uris = self.scoredict.keys()
        return sorted(uris, reverse=True, key=lambda u: self.scoredict[u])

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
