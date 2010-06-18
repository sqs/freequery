import unittest
from freequery.repository.formats import QTableFile

qtable_file1 = """http://example.com
a:b=c
x:y=z

<h1>Welcome to example</h1>
@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@
http://apple.com

<h1>Welcome to Apple</h1>"""

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

