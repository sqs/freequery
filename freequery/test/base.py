import os, unittest
from freequery.test.fixtures import dumppath


class IntegrationTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(klass):
        from freequery.client.client import Spec, FreequeryClient
        from freequery.repository.docset import Docset

        if klass.__name__ == 'IntegrationTestCase':
            return
        
        klass.spec = Spec(klass.__name__)
        klass.fqclient = FreequeryClient(klass.spec)

        # docset
        klass.docset = Docset(klass.spec.docset_name)
        klass.clean_up()
        for dumpname in klass.dumps:
            klass.docset.add_dump(dumpname, dumppath(dumpname))
        klass.docset.save()
        
        # index
        if klass.index:
            klass.fqclient.index()
            
        # rank
        if klass.rank:
            klass.fqclient.linkparse()
            niter = klass.niter if hasattr(klass, 'niter') else 2
            klass.fqclient.rank(niter=niter)

    @classmethod
    def tearDownClass(klass):
        if klass.__name__ == 'IntegrationTestCase':
            return
        klass.clean_up()

    @classmethod
    def clean_up(klass):
        if hasattr(klass, 'docset'):
            klass.docset.delete()

    def assertResultsSimilar(self, expected, actual, msg=''):
        """
        Tests whether two lists of search results are similar enough. Right
        now, this means that the relative ranking of each result is the
        same. `expected` is a list of URIs in order of decreasing score (ties
        broken by a reverse lexicographic sort on the URI itself), and `actual`
        is a list of :class:`freequery.document.Document` instances sorted by
        score.
        """
        # Sort `actual` by score, breaking ties using the URIs' lexigraphic
        # sort order.
        actual.sort(reverse=True)
        actual_uris = [doc.uri for doc in actual]
        
        self.assertEqual(
            list(expected), list(actual_uris),
            "%sexpected ranking:\n %s\n\ngot ranking:\n%s" \
            "\n\nscores:\n%s\n\ndiff:\n%s" % \
                (msg,
                 "\n".join(expected),
                 "\n".join(actual_uris),
                 "\n".join("%r\t%s" % (d.scores, d.uri) for d in actual),
                 self.__diff(expected, actual_uris)))

            
    def test_expected_results(self):
        if self.__class__.__name__ == 'IntegrationTestCase':
            return
        if not hasattr(self, 'expected_results'):
            return
        for q, expected in self.expected_results.items():
            actual = self.fqclient.query(q)
            self.assertResultsSimilar(expected, actual)

    def __diff(self, expected, result):
        import difflib
        return "\n".join(difflib.unified_diff(expected, result))
    
    def test_expected_ranking(self):
        from freequery.graph.scoredb import ScoreDB
        from freequery.document import Document
        if self.__class__.__name__ == 'IntegrationTestCase':
            return
        if not hasattr(self, 'expected_ranking'):
            return
        scoredb = ScoreDB(self.fqclient.spec.scoredb_path)
        actual = scoredb.rank()
        self.assertResultsSimilar(self.expected_ranking,
                                  [Document(uri,scores=dict(pr=pr)) \
                                   for uri,pr in actual])

    def test_against_local_pagerank(self):
        from freequery.graph.local_pagerank import pagerank
        from freequery.graph.scoredb import ScoreDB
        
        if self.__class__.__name__ == 'IntegrationTestCase':
            return

        if not getattr(self, 'check_against_local_pagerank', False):
            return

        docset = self.docset
        edges = []
        for uri in docset.doc_uris():
            doc = docset.get(uri)
            for dest_uri in doc.link_uris:
                if dest_uri in docset.doc_uris():
                    edges.append((uri, dest_uri))
        local_pr = pagerank(edges)

        scoredb = ScoreDB(self.fqclient.spec.scoredb_path)
        for uri,score in scoredb.items():
            pr = local_pr.get(uri, 0.0)
            delta = abs(pr - score)
            expected_delta = 0.01
            self.assertTrue(delta < expected_delta,
                "expected MapReduce score for URI '%s' to be almost " \
                "equal to %f (expected_delta=%.3f, delta=%f), but got %f" % \
                    (uri, pr, expected_delta, delta, score))
