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
        
        spec = Spec(klass.__name__)
        print spec
        klass.fqclient = FreequeryClient(spec)

        # docset
        klass.docset = Docset(spec.docset_name)
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
            klass.fqclient.rank()

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

    def test_expected_ranking(self):
        from freequery.graph.scoredb import ScoreDB
        if self.expected_ranking is None:
            return
        scoredb = ScoreDB(self.fqclient.spec.scoredb_path)
        result_ranking = scoredb.ranked_uris()
        self.assertEqual(list(self.expected_ranking), list(result_ranking))
