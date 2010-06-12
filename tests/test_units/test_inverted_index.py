import unittest
from freequery.index.inverted_index import InvertedIndex
from freequery.repository.document import HTMLDocument

TEST_INVERTED_INDEX_PATH = '/tmp/fq-test/invindex'

class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.invindex = InvertedIndex(TEST_INVERTED_INDEX_PATH)

        self.d1 = HTMLDocument('http://example.com', '<h1>Welcome to example</h1>')
        self.d1.docid = 1
        self.d2 = HTMLDocument('http://apple.com', '<h1>Welcome to Apple</h1>')
        self.d2.docid = 2

    def tearDown(self):
        self.invindex.clear()

    def test_lookup(self):
        self.invindex.add((self.d1,))
        self.invindex.save()
        assert [1] == self.invindex.lookup('welcome').keys()
        assert {} == self.invindex.lookup('nonexistent')

    def test_merge(self):
        # invindex #1
        self.invindex.add((self.d1,))

        # invindex #2
        invindex2 = InvertedIndex(TEST_INVERTED_INDEX_PATH+'2')
        invindex2.add((self.d2,))

        # set up invindex to merge into
        invindex3 = InvertedIndex(TEST_INVERTED_INDEX_PATH+'3')
        invindex3.merge(self.invindex, invindex2)
        assert [2] == invindex3.lookup('apple').keys()
        assert [1] == invindex3.lookup('example').keys()
        assert [1,2] == invindex3.lookup('welcome').keys()

        invindex2.clear()
        invindex3.clear()
