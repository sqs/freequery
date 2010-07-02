import simplejson

class ScoreDB(object):
    """ScoreDB reader."""

    def __init__(self, path):
        self.path = path
        self.__load()

    def __load(self):
        """Load database file into memory."""
        with open(self.path, 'rb') as dbfile:
            self.scoredict = simplejson.load(dbfile)

    def get_one(self, uri):
        """Returns the score for the document specified by `uri`."""
        return self.scoredict[uri]

    def __iter__(self):
        return self.scoredict

class ScoreDBWriter(object):

    def __init__(self, path):
        self.path = path
        self.dbfile = open(path, 'w+b')

    def set_scores(self, iterator):
        scoredict = dict(iterator)
        simplejson.dump(scoredict, self.dbfile)

    def save_and_close(self):
        self.dbfile.flush()
        self.dbfile.close()
