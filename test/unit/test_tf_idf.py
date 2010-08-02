import unittest
from freequery.index.tf_idf import TfIdf
from freequery.document import Document

class TestMapReduce(unittest.TestCase):
    def test_map(self):
        d = Document('http://a.com', 'hello there hello')
        out = list(TfIdf.map(d, None))
        expected = [('hello', 1), ('there', 1),
                    ('hello ', ('http://a.com', 2.0/3)),
                    ('there ', ('http://a.com', 1.0/3))]
        self.assertEqual(sorted(expected), sorted(out))

    def test_partition(self):
        self.assertEquals(
            TfIdf.partition('hi', 1000, None),
            TfIdf.partition('hi ', 1000, None))

    def test_reduce(self):
        from math import log
        d = Document('http://a.com', 'hello there hello')
        out = []
        class mock_reduce_out(object):
            def add(self, k, v):
                out.append((k,v))
        reduce_out = mock_reduce_out()        
        map_out = [('hello', 1), ('hello ', ('http://a.com', 2.0/3)),
                   ('there', 1), ('there ', ('http://a.com', 1.0/3))]
        # unlike in test_TfIdf.map, using doc_count=2
        TfIdf.reduce(map_out, reduce_out, {'doc_count':2})
        expected = [('hello', ('http://a.com', 2.0/3 * log(2))),
                    ('there', ('http://a.com', 1.0/3 * log(2)))]
        self.assertEqual(sorted(expected), sorted(out))
        
