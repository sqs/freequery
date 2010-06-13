import unittest
from freequery.index.inverted_index import InvertedIndexReader, InvertedIndexWriter
from freequery.index.forward_index import term_hits_to_proto
from freequery.index.forward_index_pb2 import ForwardIndexEntry as proto_ForwardIndexEntry
from freequery.repository.document import HTMLDocument

TEST_INVERTED_INDEX_PATH = '/tmp/fq-test/invindex'

def result_docids(res):
    return [p.docid for p in res]

class TestInvertedIndex(unittest.TestCase):
    
    def setUp(self):
        self.iiwriter = InvertedIndexWriter(TEST_INVERTED_INDEX_PATH)
        self.iireader = InvertedIndexReader(TEST_INVERTED_INDEX_PATH)

        self.d1 = HTMLDocument('http://example.com', '<h1>Welcome to example</h1>')
        self.d1.docid = 1
        self.e1 = term_hits_to_proto(self.d1.term_hits())
        self.e1.docid = 1
        
        self.d2 = HTMLDocument('http://apple.com', '<h1>Welcome to Apple</h1>')
        self.d2.docid = 2
        self.e2 = term_hits_to_proto(self.d2.term_hits())
        self.e2.docid = 2

    def tearDown(self):
        self.iireader.close()
        self.iiwriter.clear()
    
    def test_lookup(self):
        self.iiwriter.add(self.e1)
        self.iiwriter.save()
        assert [1] == result_docids(self.iireader.lookup('welcome'))
        assert [] == self.iireader.lookup('nonexistent')

    def test_add_two(self):
        self.iiwriter.add(self.e1)
        self.iiwriter.add(self.e2)
        self.iiwriter.save()
        assert [1,2] == result_docids(self.iireader.lookup('welcome'))
        assert [1] == result_docids(self.iireader.lookup('example'))
        assert [2] == result_docids(self.iireader.lookup('Apple'))
        assert [] == self.iireader.lookup('nonexistent')
        
