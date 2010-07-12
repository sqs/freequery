import os, unittest, StringIO
from freequery.graph.links import LinkFile, LinkFileWriter
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
        

class TestLinkFileWriter(unittest.TestCase):

    def test_writes_file1(self):
        out = StringIO.StringIO()
        writer = LinkFileWriter(out)
        docs = fixtures.dumpdocs('small1')
        writer.write(docs['http://example.com/'])
        writer.write(docs['http://example.com/about'])
        writer.write(docs['http://example.com/contact'])
        self.assertEquals(small1_links, out.getvalue())
