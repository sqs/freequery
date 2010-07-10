import unittest, StringIO
from freequery.repository.formats import QTableFile, QTableFileWriter
from freequery.test import fixtures

class TestQTableFile(unittest.TestCase):

    def test_parses_file1(self):
        parser = QTableFile(fixtures.qtable_file1.splitlines(True))
        self.assertEquals(0, parser.tell())
        example = parser.next()
        self.assertEquals(112, parser.tell())
        apple = parser.next()
        self.assertRaises(StopIteration, parser.next)
        self.assertEquals("http://example.com", example.uri)
        self.assertEquals("http://apple.com", apple.uri)
        self.assertEquals("<h1>Welcome to example</h1>", example.raw)
        self.assertEquals("<h1>Welcome to Apple</h1>", apple.raw)

class TestQTableFileWriter(unittest.TestCase):

    def test_writes_file1(self):
        out = StringIO.StringIO()
        writer = QTableFileWriter(out)
        writer.write(fixtures.example)
        writer.write(fixtures.apple)
        parser = QTableFile(out.getvalue().splitlines(True))
        self.assertEquals(fixtures.example, parser.next())
        self.assertEquals(fixtures.apple, parser.next())
