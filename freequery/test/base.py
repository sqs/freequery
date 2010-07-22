import os, unittest
from freequery.test.fixtures import dumppath


class IntegrationTestCase(unittest.TestCase):
    dumps = None
    expected_results = None
    index = True
    rank = True
    expected_ranking = None

    @classmethod
    def setUpClass(klass):
        from freequery.client.client import Spec, FreequeryClient
        from freequery.repository.docset import Docset

        if not klass.dumps:
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
            klass.fqclient.rank(niter=5)

    @classmethod
    def tearDownClass(klass):
        klass.clean_up()

    @classmethod
    def clean_up(klass):
        if hasattr(klass, 'docset'):
            klass.docset.delete()

    def test_expected_results(self):
        if not self.dumps:
            return
        for q, exp_uris in self.expected_results.items():
            result_uris = [doc.uri for doc in self.fqclient.query(q)]
            self.assertEqual(exp_uris, result_uris,
                             "expected query '%s' to yield %r, got %r" % \
                                 (q, exp_uris, result_uris))

    def __diff(self, expected, result):
        import difflib
        return "\n".join(difflib.unified_diff(expected, result))
    
    def test_expected_ranking(self):
        from freequery.graph.scoredb import ScoreDB
        if self.expected_ranking is None:
            return
        scoredb = ScoreDB(self.fqclient.spec.scoredb_path)
        result_ranking = scoredb.ranked_uris()
        self.assertEqual(
            list(self.expected_ranking), list(result_ranking),
            "expected ranking:\n %s\n\ngot ranking:\n %s" \
            "\n\nscores:\n%s\n\ndiff:\n%s" % \
                ("\n".join(self.expected_ranking),
                 "\n".join(result_ranking),
                 "\n".join(["\t".join(map(str,e)) for e in scoredb.items()]),
                 self.__diff(self.expected_ranking, result_ranking)))

    def test_against_local_pagerank(self):
        from freequery.graph.local_pagerank import pagerank
        from freequery.graph.scoredb import ScoreDB
        
        if self.rank:
            return

        docset = self.__class__.docset
        edges = []
        for uri in docset.doc_uris():
            doc = docset.get(uri)
            for dest_uri in doc.link_uris:
                if dest_uri in docset.doc_uris():
                    edges.append((uri, dest_uri))
        local_pr = pagerank(edges)

        scoredb = ScoreDB(self.fqclient.spec.scoredb_path)
        for uri,score in scoredb.items():
            delta = abs(local_pr[uri] - score)
            expected_delta = 0.05
            self.assertTrue(delta < expected_delta,
                "expected MapReduce score for URI '%s' to be almost " \
                "equal to %f (expected_delta=%.3f, delta=%f), but got %f" % \
                    (uri, local_pr[uri], expected_delta, delta, score))
