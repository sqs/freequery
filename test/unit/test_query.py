import unittest
from freequery.query import Query

class TestQuery(unittest.TestCase):

    def test_stems(self):
        self.assertEquals('welcom', Query.parse('welcome').format())
        self.assertEquals('welcom&univers', Query.parse('welcome & university').format())

    def test_eliminates_stopwords_when_stemming(self):
        qq = Query.parse('welcome & a')
        self.assertEquals('welcom&a|~a', qq.format())

    def test_non_negated_literals(self):
        qq = Query.parse('abcd & ~wxyz & efgh')
        self.assertEquals(set(['abcd', 'efgh']), set(qq.non_negated_literals()))
