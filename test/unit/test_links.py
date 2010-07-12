import os, unittest, StringIO
from freequery.graph.links import LinkFile, LinkFileOutputStream
from freequery.repository.formats import QTableFile
from freequery.test import fixtures

with open(fixtures.dumppath('small1-links'), 'rb') as lf:
    small1_links = lf.read()

class TestLinkFile(unittest.TestCase):

    def test_parses_file1(self):
        linkfile = LinkFile(small1_links.splitlines(True))
        doclinks = dict(linkfile)
        exp_doclinks = dict((uri, list(doc.link_uris())) for (uri,doc) in fixtures.dumpdocs('small1').items())
        self.assertEquals(exp_doclinks, doclinks)
        

class TestLinkFileOutputStream(unittest.TestCase):

    def test_writes_file1(self):
        out = StringIO.StringIO()
        writer = LinkFileOutputStream(out)
        docs = fixtures.dumpdocs('small1')
        writer.add('http://example.com/', docs['http://example.com/'].link_uris())
        writer.add('http://example.com/about', docs['http://example.com/about'].link_uris())
        writer.add('http://example.com/contact', docs['http://example.com/contact'].link_uris())
        self.assertEquals(small1_links, out.getvalue())
