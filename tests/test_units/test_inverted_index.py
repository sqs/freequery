import unittest
from freequery.index.inverted_index import InvertedIndex
from freequery.repository.document import HTMLDocument

TEST_INVERTED_INDEX_PATH = '/tmp/fq-test/invindex'

class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.invindex = InvertedIndex(TEST_INVERTED_INDEX_PATH)

    def tearDown(self):
        self.invindex.clear()

    def test_lookup(self):
        d1 = HTMLDocument('http://example.com', '<h1>Welcome to example</h1>')
        d1.docid = 123
        self.invindex.add((d1,))
        self.invindex.save()
        assert [123] == self.invindex.lookup('welcome').keys()
        assert {} == self.invindex.lookup('nonexistent')
