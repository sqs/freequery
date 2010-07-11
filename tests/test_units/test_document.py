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

    def test_link_uris_simple(self):
        self.assertEquals(['http://cs.stanford.edu'], list(docs.stanford.link_uris()))

    def test_title(self):
        raw = "<html><head><title>Example</title></head><body></body></html>"
        self.assertEquals('Example', Document('http://example.com/', raw).title)
    
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
            print baseuri
            d = Document(baseuri, '<a href="%s">text</a>' % href)
            print list(d.link_uris())
            link_uri = list(d.link_uris())[0]
            self.assertEquals(exp_uri, link_uri,
                              "expected (%s, %s) -> %s, got %s" % \
                                  (baseuri, href, exp_uri, link_uri))

    def test_excerpt(self):
        from freequery.query import Query
        qq = Query.parse('example')
        self.assertEquals('Welcome to example', docs.example.excerpt(qq, radius=11))
        self.assertEquals('... example', docs.example.excerpt(qq, radius=1))
        
