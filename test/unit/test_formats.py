import unittest, StringIO
from freequery.formats.warc import WARCParser, WARCWriter
from freequery.test import fixtures

class TestWARCFile(unittest.TestCase):
    def test_parses_clubweb09(self):
        warc = WARCParser(open(fixtures.dumppath('ClueWeb09_English_Sample')))
        self.assertEquals(0, warc.tell())
        
        d1 = warc.next()
        self.assertEquals(21894, warc.tell()) # TODO: check 21894
        self.assertEquals('http://www.smartwebby.com/DreamweaverTemplates/templates/business_general_template59.asp', d1.uri)
        self.assertTrue(d1.raw.startswith('<!DOCTYPE HTML PUBLIC'))
        self.assertTrue(d1.raw.endswith('<!-- InstanceEnd --></html>'))
        
        d2 = warc.next()
        self.assertEquals(43359, warc.tell()) # TODO: check 43359
        self.assertEquals('http://www.smartwebby.com/DreamweaverTemplates/templates/business_telecom_template71.asp', d2.uri)
        self.assertTrue(d2.raw.startswith('<!DOCTYPE HTML PUBLIC'))
        self.assertTrue(d2.raw.endswith('<!-- InstanceEnd --></html>'))

        # Total of 100 docs, but we already iterated over 2.
        self.assertEquals(100, len(list(warc)) + 2)

class TestWARCWriter(unittest.TestCase):

    def test_writes_file1(self):
        out = StringIO.StringIO()
        writer = WARCWriter(out)
        writer.write(fixtures.example)
        writer.write(fixtures.apple)
        out.seek(0)
        parser = WARCParser(out)
        self.assertEquals(fixtures.example, parser.next())
        self.assertEquals(fixtures.apple, parser.next())

        
