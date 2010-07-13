import unittest
from freequery.index import mapreduce
from freequery.test import fixtures


class TestDocparse(unittest.TestCase):

    def test_docparse(self):
        from StringIO import StringIO
        o = mapreduce.docparse(StringIO(fixtures.warc_file1), None, None, None)
        self.assertEquals([fixtures.example, fixtures.apple], list(o))

class TestDocdemux(unittest.TestCase):
    def test_docdemux(self):
        o = []
        for d in (fixtures.example, fixtures.apple):
            o.extend(list(mapreduce.docdemux(d, None)))
        exp = [('welcom', 'http://example.com'), ('exampl', 'http://example.com'), ('welcom', 'http://apple.com'), ('appl', 'http://apple.com')]
        self.assertEquals(sorted(exp), sorted(o))
