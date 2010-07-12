import os, unittest
from freequery.client.client import Spec, FreequeryClient
from freequery.repository.docset import Docset

class IntegrationTestCase(unittest.TestCase):
    dumps = None
    expected_results = None
    index = True
    rank = True
    
    def setUp(self):
        if not self.dumps:
            return
        
        spec = Spec(self.__class__.__name__)
        self.fqclient = FreequeryClient(spec)

        # docset
        self.docset = Docset(spec.docset_name)
        self.clean_up()
        for dumpname in self.dumps:
            path = os.path.join(os.path.dirname(__file__), "../../test/dumps", dumpname)
            self.docset.add_dump(dumpname, path)
        self.docset.save()
        
        # index
        if self.index:
            self.fqclient.index()
            
        # rank
        if self.rank:
            self.fqclient.linkparse()
            self.fqclient.rank()
    
    def tearDown(self):
        self.clean_up()
        
    def clean_up(self):
        if hasattr(self, 'docset'):
            self.docset.delete()

    def test_expected_results(self):
        if not self.dumps:
            return
        for q, exp_uris in self.expected_results.items():
            result_uris = [doc.uri for doc in self.fqclient.query(q)]
            self.assertEqual(exp_uris, result_uris,
                             "expected query '%s' to yield %r, got %r" % \
                                 (q, exp_uris, result_uris))
