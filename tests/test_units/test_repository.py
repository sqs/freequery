import os, unittest
from freequery.repository import Repository
from freequery.document import Document
from freequery.test import fixtures as docs

TEST_REPOSITORY_PATH = '/tmp/fq-test/'

class TestRepository(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_REPOSITORY_PATH):
            os.makedirs(TEST_REPOSITORY_PATH)
        self.repos = Repository(TEST_REPOSITORY_PATH)

    def tearDown(self):
        self.repos.clear()

    def test_adds(self):
        i = self.repos.add(docs.example)
        assert docs.example == self.repos.get(i)

    def test_adds_two(self):
        i = self.repos.add(docs.example)
        j = self.repos.add(docs.apple)
        assert docs.example == self.repos.get(i)
        assert docs.apple == self.repos.get(j)

    def test_persists(self):
        i = self.repos.add(docs.example)
        self.repos.close()
        self.repos = Repository(TEST_REPOSITORY_PATH)
        assert docs.example == self.repos.get(i)

    def test_reopenable_for_appends(self):
        i = self.repos.add(docs.example)
        self.repos.close()
        self.repos = Repository(TEST_REPOSITORY_PATH)
        j = self.repos.add(docs.apple)
        assert docs.example == self.repos.get(i)
        assert docs.apple == self.repos.get(j)

    def test_iterates(self):
        i = self.repos.add(docs.example)
        j = self.repos.add(docs.apple)
        self.repos.docindex.save()
        iter_docs = list(self.repos.__iter__())
        assert [docs.example, docs.apple] == iter_docs
