from freequery.test import IntegrationTestCase, fixtures as docs
from freequery.repository.repository import Repository
from freequery.index.forward_index import ForwardIndex
from freequery.index.inverted_index import InvertedIndexWriter, InvertedIndexReader

TEST_REPOSITORY_PATH = "/tmp/fq-test/"

class TestIntegration(IntegrationTestCase):

    def __run_test(self, docs, query, expected_result_uris):
        repos = Repository(TEST_REPOSITORY_PATH)
        fwdindex = ForwardIndex(TEST_REPOSITORY_PATH + 'fwdindex')
        iiwriter = InvertedIndexWriter(TEST_REPOSITORY_PATH + 'invindex')
        for doc in docs:
            docid = repos.add(doc)
            doc.docid = docid
            fwdindex.add(doc)            
        
        for e in fwdindex:
            iiwriter.add(e)
        iiwriter.finish()
        fwdindex.close()

        iireader = InvertedIndexReader(TEST_REPOSITORY_PATH + 'invindex')
        result_uris = [repos.get(e.docid).uri for e in iireader.lookup(query)]
        repos.close()
        self.assertEquals(list(expected_result_uris), result_uris)
        
    def test_integration1(self):
        self.__run_test((docs.example, docs.apple), 'example', ('http://example.com',))
