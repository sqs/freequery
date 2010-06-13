import unittest
from freequery.index.forward_index import ForwardIndex
from freequery.repository.document import Document

TEST_FORWARD_INDEX_PATH = '/tmp/fq-test/fwdindex'

class TestForwardIndex(unittest.TestCase):

    def setUp(self):
        self.fwdindex = ForwardIndex(TEST_FORWARD_INDEX_PATH)
        self.d1 = Document('http://example.com', '<h1>Welcome to example</h1>', 1)
        self.d2 = Document('http://apple.com', '<h1>Welcome to Apple</h1>', 2)
        
    def tearDown(self):
        self.fwdindex.clear()

    def test_iterates(self):
        self.fwdindex.add(self.d1)
        self.fwdindex.add(self.d2)
        orig_docs = [self.d1, self.d2]
        orig_list = map(lambda d: (d.docid, len(d.term_hits())), orig_docs)
        iter_entries = list(self.fwdindex.__iter__())
        iter_list = map(lambda e: (e.docid, len(e.term_hits)), iter_entries)
        assert orig_list == iter_list
        orig_terms = map(lambda d: map(lambda th: th[0], d.term_hits().items()), orig_docs)
        iter_terms = map(lambda e: map(lambda th: th.term, e.term_hits), iter_entries)
        assert orig_terms == iter_terms

    def test_persists(self):
        self.fwdindex.add(self.d1)
        self.fwdindex.close()
        self.fwdindex = ForwardIndex(TEST_FORWARD_INDEX_PATH)
        assert [self.d1.docid] == \
               map(lambda d: d.docid, list(self.fwdindex.__iter__()))
        
