import unittest
from freequery.query import Query

class TestQuery(unittest.TestCase):

    def test_stems(self):
        self.assertEquals('welcom', Query.parse('welcome').format())
        self.assertEquals('welcom&univers', Query.parse('welcome & university').format())
