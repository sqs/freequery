import unittest
from freequery.document import Document
from freequery.test import fixtures as docs


class TestDocument(unittest.TestCase):

    def test_eq(self):
        assert Document('http://example.com', '<h1>Welcome to example</h1') == \
               Document('http://example.com', '<h1>Welcome to example</h1')
        assert Document('http://example.com', '<h1>Welcome to example</h1') != \
               Document('http://apple.com', '<h1>Welcome to Apple</h1>')

        
class TestHTMLDocument(unittest.TestCase):

    def test_tokens(self):
        assert ['Welcome', 'to', 'example'] == docs.example.tokens()
        
    def test_terms(self):
        assert ['welcom', 'exampl'] == docs.example.terms()
        
