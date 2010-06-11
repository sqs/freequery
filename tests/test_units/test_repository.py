import os, unittest
from freequery.repository.repository import Repository
from freequery.repository.document import Document

TEST_REPOSITORY_PATH = '/tmp/fq-test/'

class TestRepository(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_REPOSITORY_PATH):
            os.makedirs(TEST_REPOSITORY_PATH)
        self.repos = Repository(TEST_REPOSITORY_PATH)
        self.doc = Document('http://example.com', {'title': 'Example'})

    def tearDown(self):
        self.repos.clear()

    def test_adds(self):
        self.repos.add(self.doc)
        assert self.doc == self.repos.get('http://example.com')

    def test_persists(self):
        self.repos.add(self.doc)
        self.repos.close()
        self.repos = Repository(TEST_REPOSITORY_PATH)
        assert self.doc == self.repos.get('http://example.com')

