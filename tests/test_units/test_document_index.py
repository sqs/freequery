import unittest
from freequery.repository.document_index import DocumentIndex

TEST_DOCUMENT_INDEX_PATH = "/tmp/fq-test.docindex"

class TestDocumentIndex(unittest.TestCase):

    def setUp(self):
        self.docindex = DocumentIndex(TEST_DOCUMENT_INDEX_PATH)

    def tearDown(self):
        self.docindex.clear()

    def test_notfound(self):
        assert 'http://apple.com' not in self.docindex
        self.assertRaises(KeyError, lambda: self.docindex['http://stanford.edu'])
    
    def test_add(self):
        assert 'http://example.com' not in self.docindex
        self.docindex.add('http://example.com')
        assert 'http://example.com' in self.docindex

    def test_unique_docids(self):
        i = self.docindex.add('http://example.com')
        j = self.docindex.add('http://stanford.edu')
        assert i != j

    def test_no_duplicate_uris(self):
        i = self.docindex.add('http://example.com')
        j = self.docindex.add('http://example.com')
        assert i == j

    def test_persists(self):
        i = self.docindex.add('http://example.com')
        self.docindex.close()
        self.docindex = DocumentIndex(TEST_DOCUMENT_INDEX_PATH)
        j = self.docindex['http://example.com']
        assert i == j

    def test_iterates_docids(self):
        i = self.docindex.add('http://example.com')
        j = self.docindex.add('http://apple.com')
        assert list(self.docindex.docids()) == [i, j]
        
