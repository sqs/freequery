import unittest
from freequery.index.forward_index import ForwardIndex
from freequery.document import Document
from freequery.test import fixtures as docs

TEST_FORWARD_INDEX_PATH = '/tmp/fq-test/fwdindex'

class TestForwardIndex(unittest.TestCase):

    def setUp(self):
        self.fwdindex = ForwardIndex(TEST_FORWARD_INDEX_PATH)
        
    def tearDown(self):
        self.fwdindex.clear()

    def test_iterates(self):
        self.fwdindex.add(docs.example)
        self.fwdindex.add(docs.apple)
        orig_docs = [docs.example, docs.apple]
        orig_list = map(lambda d: (d.docid, len(d.term_hits())), orig_docs)
        iter_entries = list(self.fwdindex.__iter__())
        iter_list = map(lambda e: (e.docid, len(e.term_hits)), iter_entries)
        assert orig_list == iter_list
        orig_terms = map(lambda d: map(lambda th: th[0], d.term_hits().items()), orig_docs)
        iter_terms = map(lambda e: map(lambda th: th.term, e.term_hits), iter_entries)
        assert orig_terms == iter_terms

    def test_persists(self):
        self.fwdindex.add(docs.example)
        self.fwdindex.close()
        self.fwdindex = ForwardIndex(TEST_FORWARD_INDEX_PATH)
        assert [docs.example.docid] == \
               map(lambda d: d.docid, list(self.fwdindex.__iter__()))
        
