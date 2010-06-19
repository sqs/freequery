import unittest
from freequery.repository.formats import QTableFile
from freequery.test.fixtures import qtable_file1

class TestQTableFile(unittest.TestCase):

    def test_parses_file1(self):
        parser = QTableFile(qtable_file1.splitlines(True))
        example = parser.next()
        apple = parser.next()
        self.assertRaises(StopIteration, parser.next)
        self.assertEquals("http://example.com", example.uri)
        self.assertEquals("http://apple.com", apple.uri)
        self.assertEquals("<h1>Welcome to example</h1>\n", example.raw)
        self.assertEquals("<h1>Welcome to Apple</h1>", apple.raw)

