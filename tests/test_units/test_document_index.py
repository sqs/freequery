import unittest
from freequery.repository.document_index import DocumentIndex, RepositoryPointer

TEST_DOCUMENT_INDEX_PATH = "/tmp/fq-test/"

def rptr(file, ofs): return RepositoryPointer(file=file, ofs=ofs)

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
        self.docindex.add('http://example.com', rptr(0,0))
        assert 'http://example.com' in self.docindex

    def test_unique_docids(self):
        i = self.docindex.add('http://example.com', rptr(0,0))
        j = self.docindex.add('http://stanford.edu', rptr(0,1))
        assert i != j

    def test_no_duplicate_uris(self):
        self.docindex.add('http://example.com', rptr(0,0))
        add_dup = lambda: self.docindex.add('http://example.com', rptr(0,3))
        self.assertRaises(NotImplementedError, add_dup)

    def test_persists(self):
        i = self.docindex.add('http://example.com', rptr(1,2))
        self.docindex.save()
        self.docindex.close()
        self.docindex = DocumentIndex(TEST_DOCUMENT_INDEX_PATH)
        j = self.docindex['http://example.com']
        assert j.ptr == rptr(1,2)

    def test_iterates_docids(self):
        i = self.docindex.add('http://example.com', rptr(0,0))
        j = self.docindex.add('http://apple.com', rptr(0,1))
        assert list(self.docindex.docids()) == [i, j]
        
