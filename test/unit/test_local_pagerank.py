import unittest
from freequery.graph.local_pagerank import pagerank

class TestLocalPagerank(unittest.TestCase):

    def assertRanking(self, expected_ranking, edges):
        from operator import itemgetter
        from math import fsum
        pr = pagerank(edges)

        # should sum to 1
        self.assertAlmostEqual(1.0, fsum(pr.values()))

        # should be in correct order
        ranking = map(itemgetter(0),
                      sorted(pr.items(), key=itemgetter(1), reverse=True))
        self.assertEqual(list(expected_ranking), list(ranking),
                         "expected Web graph with edges %r to have ranking " \
                         "%r, but got ranking %r (pageranks: %r)" % \
                         (edges, expected_ranking, ranking, pr))
    
    def test_simple1(self):
        edges = [(1,2), (1,3), (2,3), (3,1)]
        self.assertRanking((3,1,2), edges)
        
        
