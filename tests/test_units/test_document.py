import unittest
from freequery.repository.document import Document


class TestDocument(unittest.TestCase):

    def test_eq(self):
        assert Document('http://example.com', {'title': 'Example'}) == \
               Document('http://example.com', {'title': 'Example'})
        assert Document('http://example.com', {'title': 'Example'}) != \
               Document('http://apple.com', {'title': 'Apple'})

    def test_pack(self):
        d1 = Document('http://example.com', '<h1>Welcome to example</h1>')
        proto_d1 = Document.from_proto_string(d1.to_proto_string())
        assert d1 == proto_d1

class TestHTMLDocument(unittest.TestCase):

    def setUp(self):
        self.d1 = Document('http://example.com', '<h1>Welcome to example</h1>')
        self.d1.make_typed('text/html')

    def test_tokens(self):
        assert ['Welcome', 'to', 'example'] == self.d1.tokens()
        
