import unittest
from freequery.index.inverted_index import InvertedIndex
from freequery.index.forward_index import term_hits_to_proto
from freequery.index.forward_index_pb2 import ForwardIndexEntry as proto_ForwardIndexEntry
from freequery.repository.document import HTMLDocument

TEST_INVERTED_INDEX_PATH = '/tmp/fq-test/invindex'

def result_docids(res):
    return dict(res).keys()

class TestInvertedIndex(unittest.TestCase):
    
    def setUp(self):
        self.invindex = InvertedIndex(TEST_INVERTED_INDEX_PATH)

        self.d1 = HTMLDocument('http://example.com', '<h1>Welcome to example</h1>')
        self.d1.docid = 1
        self.e1 = term_hits_to_proto(self.d1.term_hits())
        self.e1.docid = 1
        
        self.d2 = HTMLDocument('http://apple.com', '<h1>Welcome to Apple</h1>')
        self.d2.docid = 2
        self.e2 = term_hits_to_proto(self.d2.term_hits())
        self.e2.docid = 2

    def tearDown(self):
        self.invindex.clear()

    def test_lookup(self):
        self.invindex.add(self.e1)
        self.invindex.save()
        assert [1] == result_docids(self.invindex.lookup('welcome'))
        assert [] == self.invindex.lookup('nonexistent')

    def test_merge(self):
        # invindex #1
        self.invindex.add(self.e1)

        # invindex #2
        invindex2 = InvertedIndex(TEST_INVERTED_INDEX_PATH+'2')
        invindex2.add(self.e2)

        # set up invindex to merge into
        invindex3 = InvertedIndex(TEST_INVERTED_INDEX_PATH+'3')
        invindex3.merge(self.invindex, invindex2)
        assert [2] == result_docids(invindex3.lookup('apple'))
        assert [1] == result_docids(invindex3.lookup('example'))
        assert [1,2] == result_docids(invindex3.lookup('welcome'))

        invindex2.clear()
        invindex3.clear()
