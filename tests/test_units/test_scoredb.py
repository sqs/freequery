import unittest
from freequery.graph.scoredb import ScoreDB, ScoreDBWriter

TEST_SCOREDB_PATH = "/tmp/fq-scoredb"

class TestScoreDB(unittest.TestCase):
    sample_scores = {
        'http://example.com/': 0.05,
        'http://example.com/a.html': 0.04,
        'http://stanford.edu/': 0.02,
    }

    def __write_fixture(self):
        dbw = ScoreDBWriter(TEST_SCOREDB_PATH)
        dbw.set_scores(self.sample_scores)
        dbw.save_and_close()

    def test_reads_writes(self):
        self.__write_fixture()
        scoredb = ScoreDB(TEST_SCOREDB_PATH)
        self.assertAlmostEqual(0.05, scoredb.get_one('http://example.com/'))
        self.assertAlmostEqual(0.04, scoredb.get_one('http://example.com/a.html'))
        self.assertAlmostEqual(0.02, scoredb.get_one('http://stanford.edu/'))

    def test_iterates(self):
        self.__write_fixture()
        scoredb = ScoreDB(TEST_SCOREDB_PATH)
        self.assertEquals(self.sample_scores, scoredb.__iter__())
