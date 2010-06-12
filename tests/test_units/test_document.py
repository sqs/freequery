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
        assert d1 == Document.unpack(d1.pack())
        
