import unittest
from freequery.document import Document
from freequery.query import Query
from freequery.test import fixtures


class TestDocument(unittest.TestCase):

    def test_score(self):
        self.assertAlmostEqual(1.0,
                               Document('http://example.com', scores=dict(pr=1.0)).scores['pr'])
        self.assertFalse(hasattr(Document('http://example.com'), 'scores'))

    def test_eq(self):
        assert Document('http://example.com', '<h1>Welcome to example</h1') == \
               Document('http://example.com', '<h1>Welcome to example</h1')
        assert Document('http://example.com', '<h1>Welcome to example</h1') != \
               Document('http://apple.com', '<h1>Welcome to Apple</h1>')

    def test_lt(self):
        d1 = Document('http://a.com', scores=dict(pr=1.0))
        d2 = Document('http://b.com', scores=dict(pr=1.0))
        d3 = Document('http://z.com', scores=dict(pr=5.0))
        self.assertEquals([d3, d1, d2], sorted([d3,d2,d1], reverse=True))
        
class TestHTMLDocument(unittest.TestCase):
       
    def test_tokens(self):
        assert ['Welcome', 'to', 'example'] == fixtures.example.tokens()
        
    def test_terms(self):
        assert ['welcom', 'exampl'] == fixtures.example.terms()

    def test_term_frequences(self):
        self.assertEquals(dict(welcom=1, exampl=1), fixtures.example.term_frequencies())

    def test_link_uris_simple(self):
        self.assertEquals(['http://cs.stanford.edu'], list(fixtures.stanford.link_uris))

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
            print list(d.link_uris)
            link_uri = list(d.link_uris)[0]
            self.assertEquals(exp_uri, link_uri,
                              "expected (%s, %s) -> %s, got %s" % \
                                  (baseuri, href, exp_uri, link_uri))

    def test_cache_link_uris(self):
        doc = Document('http://stanford.edu/', '<a href="a.html">a</a>')
        self.assertEquals(['http://stanford.edu/a.html'], doc.link_uris)
        doc.cache_link_uris(['http://stanford.edu/other.html'])
        self.assertEquals(['http://stanford.edu/other.html'], doc.link_uris)

    def test_excerpt(self):
        qq = Query.parse('example')
        self.assertEquals('Welcome to example', fixtures.example.excerpt(qq, radius=11))
        self.assertEquals('... example', fixtures.example.excerpt(qq, radius=1))

    def test_excerpt_lowercases(self):
        qq = Query.parse('welcome')
        self.assertEquals('Welcome to example', fixtures.example.excerpt(qq, radius=20))

    def test_empty_doc(self):
        emptydoc1 = fixtures.dumpdocs('empty-doc')['http://aero-comlab.stanford.edu/sichoi/tet_mesh.html']
        # should not raise 'ParserError: Document is empty'
        self.assertEquals([], emptydoc1.link_uris)
        # should not raise "AttributeError: 'NoneType' object has no attribute
        # 'text_content'"
        self.assertEquals([], emptydoc1.tokens())

    def test_raw_None(self):
        rawNone = fixtures.dumpdocs('raw-None')['http://cse.stanford.edu/class/cs201/projects-00-01/napster/index.html']
        self.assertEquals(None, rawNone.html_parser)

    def test_pickleable(self):
        # The lxml HTML parser isn't pickleable, so remove it first.
        import pickle
        d = Document('http://a.com', '<body><b>hello there</b></body>')
        d.html_parser
        dp = pickle.loads(pickle.dumps(d))
        self.assertEquals(d, dp)

    def test_pickleable_without_html_parser(self):
        # But check that even without the HTML parser, this is pickleable.
        import pickle
        d = Document('http://a.com', '<body><b>hello there</b></body>')
        dp = pickle.loads(pickle.dumps(d))
        self.assertEquals(d, dp)
        
        
