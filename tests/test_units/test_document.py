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

    def test_term_frequences(self):
        self.assertEquals(dict(welcom=1, exampl=1), docs.example.term_frequencies())

    def test_link_uris(self):
        self.assertEquals(['http://cs.stanford.edu'], list(docs.stanford.link_uris()))

    # base URI tests
    base_uri_data = {
        # trivial
        ('http://example.com/', None): 'http://example.com/',
        # absolute root base
        ('http://example.com/', 'http://example.com/'): 'http://example.com/',
        # trivial dir
        ('http://example.com/dir/', None): 'http://example.com/dir/',
        # absolute dir base
        ('http://example.com/', 'http://example.com/dir/'): 'http://example.com/dir/',
        # trivial file
        ('http://example.com/file', None): 'http://example.com/',
        # absolute root base
        ('http://example.com/file', 'http://example.com/'): 'http://example.com/',
    }

    def test_base_uri(self):
        for (uri,basehref),exp_base_uri in self.base_uri_data.items():
            raw = ""
            if basehref:
                raw = "<html><head><base href='%s'></head><body></body></html>" % basehref
            d = Document(uri, raw)
            base_uri = d.base_uri()
            self.assertEquals(exp_base_uri, base_uri,
                              "expected (%s, %s) -> %s, got %s" % \
                                  (uri, basehref, exp_base_uri, base_uri))

    # link URI tests                              
    link_uri_data = {
        # (base uri, a href) -> link uri
        ('http://example.com/', 'http://example.com/a.html'): 'http://example.com/a.html',
        ('http://example.com/', 'b.html'): 'http://example.com/b.html',
        ('http://example.com/c.html', 'd.html'): 'http://example.com/d.html',
        ('http://example.com/x/', 'y.html'): 'http://example.com/x/y.html',
        ('http://example.com/x/z/', '/m.html'): 'http://example.com/m.html',
        ('http://example.com/x/z/', '/h/n.html'): 'http://example.com/h/n.html',
    }

    def test_link_uris(self):
        for (baseuri,href),exp_uri in self.link_uri_data.items():
            d = Document(baseuri, '<a href="%s">text</a>' % href)
            link_uri = list(d.link_uris())[0]
            self.assertEquals(exp_uri, link_uri,
                              "expected (%s, %s) -> %s, got %s" % \
                                  (baseuri, href, exp_uri, link_uri))
