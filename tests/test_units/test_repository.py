import os, unittest
from freequery.repository.repository import Repository
from freequery.repository.document import Document

TEST_REPOSITORY_PATH = '/tmp/fq-test/'

class TestRepository(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_REPOSITORY_PATH):
            os.makedirs(TEST_REPOSITORY_PATH)
        self.repos = Repository(TEST_REPOSITORY_PATH)
        self.doc = Document('http://example.com', '<h1>Welcome to example</h1>')

    def tearDown(self):
        self.repos.clear()

    def test_adds(self):
        i = self.repos.add(self.doc)
        assert self.doc == self.repos.get(i)

    def test_adds_two(self):
        i = self.repos.add(self.doc)
        doc2 = Document('http://apple.com', '<h1>Welcome to Apple</h1>')
        j = self.repos.add(doc2)
        assert self.doc == self.repos.get(i)
        assert doc2 == self.repos.get(j)

    def test_persists(self):
        i = self.repos.add(self.doc)
        self.repos.close()
        self.repos = Repository(TEST_REPOSITORY_PATH)
        assert self.doc == self.repos.get(i)

    def test_reopenable_for_appends(self):
        i = self.repos.add(self.doc)
        doc2 = Document('http://apple.com', '<h1>Welcome to Apple</h1>')
        self.repos.close()
        self.repos = Repository(TEST_REPOSITORY_PATH)
        j = self.repos.add(doc2)
        assert self.doc == self.repos.get(i)
        assert doc2 == self.repos.get(j)

    def test_iterates(self):
        i = self.repos.add(self.doc)
        doc2 = Document('http://apple.com', '<h1>Welcome to Apple</h1>')
        j = self.repos.add(doc2)
        self.repos.docindex.save()
        iter_docs = list(self.repos.__iter__())
        assert [self.doc, doc2] == iter_docs
