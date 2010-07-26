
def score_pagerank_cmp(a, b):
    return cmp(a['pagerank'], b['pagerank'])

class Score(object):

    def __init__(self, **scores):
        """
        Creates a new `Score` object from `scores`, a set of key-value pairs
        like `{'pagerank': 0.05, 'tfidf': 3.5}`.
        """
        self.info = scores

    def product(self):
        p = 1.0
        for v in self.info.values():
            p *= v
        return p

    def __cmp__(self, other):
        raise NotImplementedError

    def __getitem__(self, k):
        return self.info[k]

    def __setitem__(self, k, v):
        self.info[k] = v

    def __str__(self):
        return str(self.info)

    __unicode__ = __str__
    __repr__ = __str__
