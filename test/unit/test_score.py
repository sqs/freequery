import unittest
from freequery.document.score import Score, score_pagerank_cmp

class TestScore(unittest.TestCase):

    def test_product(self):
        self.assertAlmostEqual(5.0, Score(pagerank=0.25, tfidf=20).product())

    def test_getitem(self):
        self.assertEqual(2.0, Score(pagerank=2.0)['pagerank'])

    def test_setitem(self):
        s = Score()
        s['pagerank'] = 3.0
        self.assertEqual(3.0, s['pagerank'])

    def test_score_pagerank_cmp(self):
        s1, s2 = Score(pagerank=1.0), Score(pagerank=2.0) # s1 < s2
        self.assertTrue(score_pagerank_cmp(s1, s2) < 0)
