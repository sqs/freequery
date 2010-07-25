import unittest
from freequery.index.mapreduce import *
from freequery.test import fixtures
from freequery.document import Document


class TestDocparse(unittest.TestCase):

    def test_docparse(self):
        from StringIO import StringIO
        o = docparse(StringIO(fixtures.warc_file1), None, None, None)
        self.assertEquals([fixtures.example, fixtures.apple], list(o))

class TestDocdemux(unittest.TestCase):
    def test_docdemux(self):
        o = []
        for d in (fixtures.example, fixtures.apple):
            o.extend(list(docdemux(d, None)))
        exp = [('welcom', 'http://example.com'), ('exampl', 'http://example.com'), ('welcom', 'http://apple.com'), ('appl', 'http://apple.com')]
        self.assertEquals(sorted(exp), sorted(o))

class TestMapReduce(unittest.TestCase):

    def test_doc_term_map(self):
        d = Document('http://a.com', 'hello there hello')
        out = list(doc_term_map(d, None))
        expected = [('hello', 1), ('there', 1), ('hello', (d, 2)),
                    ('there', (d, 1))]
        self.assertEqual(sorted(expected), sorted(out))

    def test_doc_term_reduce(self):
        d = Document('http://a.com', 'hello there hello')
        out = []
        class mock_reduce_out(object):
            def add(self, k, v):
                out.append((k,v))
        reduce_out = mock_reduce_out()        
        map_out = [('hello', 1), ('hello', (d, 2)),
                   ('there', 1), ('there', (d, 1))]
        # unlike in test_doc_term_map, using doc_count=2
        doc_term_reduce(map_out, reduce_out, {'doc_count':2})
        expected = [('hello', (d, 2.0 * 2)), ('there', (d, 1.0 * 2))]
        self.assertEqual(sorted(expected), sorted(out))
        
