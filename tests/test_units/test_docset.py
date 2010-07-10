import os, unittest
from freequery.repository.docset import Docset
from freequery.test import fixtures

WROTE_DUMP = False
dump1 = '/tmp/test-fq-docset-dump1'
dump2 = '/tmp/test-fq-docset-dump2'

class TestDocset(unittest.TestCase):
    def setUp(self):
        global WROTE_DUMP
        if not WROTE_DUMP:
            self.__write_dumps()
            WROTE_DUMP = True
        self.docset = Docset('fq-test')

    def tearDown(self):
        self.docset.delete()

    def test_delete(self):
        self.docset.add_dump('d1', dump1)
        self.docset.delete()
        # If this test is failing, then we might need to wait for DDFS garbage
        # collection here, but it seems to work fine for now.
        self.assertFalse('d1' in self.docset.dump_names_without_doc_counts())
        
    def test_add_dump(self):
        self.docset.add_dump('d1', dump1)

        # check that it's in list of dumps
        self.assertTrue('d1' in self.docset.dump_names_without_doc_counts())

        # check accessible over http
        from disco.util import urlresolve
        import urllib2
        uri = list(self.docset.dump_uris())[0]
        httpuri = urlresolve(uri)
        d = urllib2.urlopen(httpuri).read()
        self.assertEquals(d, fixtures.qtable_file1)

    def test_exists(self):
        self.assertFalse(self.docset.exists())
        self.docset.add_dump('d1', dump1)
        self.assertTrue(self.docset.exists())

    def test_doc_count(self):
        self.assertEquals(0, self.docset.doc_count())
        self.docset.add_dump('d1', dump1)
        self.assertEquals(2, self.docset.doc_count())
        self.docset.add_dump('d2', dump2)
        self.assertEquals(4, self.docset.doc_count())

    def test_get_pos(self):
        self.docset.add_dump('d1', dump1)
        self.docset.add_dump('d2', dump2)
        pos1 = self.docset.get_pos('http://example.com')
        self.assertEquals(('d1', 0, 112), pos1)
        pos2 = self.docset.get_pos('http://apple.com')
        self.assertEquals(('d1', 112, 43), pos2)
        pos3 = self.docset.get_pos('http://example.com/m.html')
        self.assertEquals(('d2', 0, 98), pos3)
        pos4 = self.docset.get_pos('http://example.com/z.html')
        self.assertEquals(('d2', 98, 45), pos4)
      
    def test_get(self):
        self.docset.add_dump('d1', dump1)
        self.docset.add_dump('d2', dump2)
        self.assertEquals(fixtures.example, self.docset.get('http://example.com'))
        self.assertEquals(fixtures.apple, self.docset.get('http://apple.com'))
        self.assertEquals(fixtures.examplez, self.docset.get('http://example.com/z.html'))

    def __write_dumps(self):
        with open(dump1, 'w+b') as f:
            f.write(fixtures.qtable_file1)
        with open(dump2, 'w+b') as f:
            f.write(fixtures.qtable_file2)
