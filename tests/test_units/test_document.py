import unittest
from freequery.repository.document import Document
from tests.fixtures import docs


class TestDocument(unittest.TestCase):

    def test_eq(self):
        assert Document('http://example.com', '<h1>Welcome to example</h1') == \
               Document('http://example.com', '<h1>Welcome to example</h1')
        assert Document('http://example.com', '<h1>Welcome to example</h1') != \
               Document('http://apple.com', '<h1>Welcome to Apple</h1>')

    def test_pack(self):
        proto_doc = Document.from_proto_string(docs.example.to_proto_string())
        assert docs.example == proto_doc

class TestHTMLDocument(unittest.TestCase):

    def test_tokens(self):
        assert ['Welcome', 'to', 'example'] == docs.example.tokens()
        
