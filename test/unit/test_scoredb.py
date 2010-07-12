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

    def setUp(self):
        self.__write_fixture()
        self.scoredb = ScoreDB(TEST_SCOREDB_PATH)

    def test_reads_writes(self):
        self.assertAlmostEqual(0.05, self.scoredb.get_one('http://example.com/'))
        self.assertAlmostEqual(0.04, self.scoredb.get_one('http://example.com/a.html'))
        self.assertAlmostEqual(0.02, self.scoredb.get_one('http://stanford.edu/'))

    def test_iterates(self):
        self.assertEquals(sorted(self.sample_scores.items()), sorted(self.scoredb.items()))

    def test_ranked_uris(self):
        self.assertEquals(['http://example.com/', 'http://example.com/a.html', 'http://stanford.edu/'], self.scoredb.ranked_uris())
        self.assertEquals(['http://example.com/', 'http://stanford.edu/'], self.scoredb.ranked_uris(['http://stanford.edu/', 'http://example.com/']))
        
