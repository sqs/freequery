import unittest
from freequery.index import mapreduce
from freequery.test.fixtures import qtable_file1


class TestDocparse(unittest.TestCase):

    def test_docparse(self):
        o = mapreduce.docparse(qtable_file1.splitlines(True), None, None, None)
        self.assertEquals([('welcom', 'http://example.com'), ('exampl', 'http://example.com'), ('welcom', 'http://apple.com'), ('appl', 'http://apple.com')], list(o))
