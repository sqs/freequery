import unittest
from freequery.index.mapreduce import *
from freequery.test import fixtures
from freequery.document import Document


class TestDocparse(unittest.TestCase):

    def test_docparse(self):
        from StringIO import StringIO
        o = docparse(StringIO(fixtures.warc_file1), None, None, None)
        self.assertEquals([fixtures.example, fixtures.apple], list(o))

class TestMapReduce(unittest.TestCase):

    def test_doc_tfidf_map(self):
        d = Document('http://a.com', 'hello there hello')
        out = list(doc_tfidf_map(d, None))
        expected = [('hello', 1), ('there', 1),
                    ('hello ', ('http://a.com', 2.0/3)),
                    ('there ', ('http://a.com', 1.0/3))]
        self.assertEqual(sorted(expected), sorted(out))

    def test_doc_tfidf_partition(self):
        self.assertEquals(
            doc_tfidf_partition('hi', 1000, None),
            doc_tfidf_partition('hi ', 1000, None))

    def test_doc_tfidf_reduce(self):
        from math import log
        d = Document('http://a.com', 'hello there hello')
        out = []
        class mock_reduce_out(object):
            def add(self, k, v):
                out.append((k,v))
        reduce_out = mock_reduce_out()        
        map_out = [('hello', 1), ('hello ', ('http://a.com', 2.0/3)),
                   ('there', 1), ('there ', ('http://a.com', 1.0/3))]
        # unlike in test_doc_tfidf_map, using doc_count=2
        doc_tfidf_reduce(map_out, reduce_out, {'doc_count':2})
        expected = [('hello', ('http://a.com', 2.0/3 * log(2))),
                    ('there', ('http://a.com', 1.0/3 * log(2)))]
        self.assertEqual(sorted(expected), sorted(out))
        
