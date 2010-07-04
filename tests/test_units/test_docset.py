import os, unittest
from freequery.repository.docset import Docset
from freequery.test import fixtures

WROTE_DUMP = False
dump1 = '/tmp/test-fq-docset-dump'

class TestDocset(unittest.TestCase):
    def setUp(self):
        global WROTE_DUMP
        if not WROTE_DUMP:
            self.__write_dump()
            WROTE_DUMP = True
        self.docset = Docset('fq-test')

    def test_delete(self):
        self.docset.add_dump('d1', dump1)
        self.docset.delete()
        # If this test is failing, then we might need to wait for DDFS garbage
        # collection here, but it seems to work fine for now.
        self.assertFalse('d1' in self.docset.dump_names())
        
    def test_add_dump(self):
        self.docset.add_dump('d1', dump1)

        # check that it's in list of dumps
        self.assertTrue('d1' in self.docset.dump_names())

        # check accessible over http
        from disco.ddfs import DDFS
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

    def __write_dump(self):
        with open(dump1, 'w+b') as f:
            f.write(fixtures.qtable_file1)
