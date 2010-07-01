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

#    def test_list(self):
#        assert False

    def test_add(self):
        self.docset.add_dump('d1', dump1)
        # check that it was uploaded
        self.assertTrue('d1' in self.docset.dump_names())

    def __write_dump(self):
        with open(dump1, 'w+b') as f:
            f.write(fixtures.qtable_file1)
