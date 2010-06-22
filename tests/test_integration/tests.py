from freequery.test import IntegrationTestCase, fixtures as docs

class TestIntegration(IntegrationTestCase):

    def __run_test(self, docs, query, expected_result_uris):
	assert False
        result_uris = [repos.get(e.docid).uri for e in iireader.lookup(query)]
        repos.close()
        self.assertEquals(list(expected_result_uris), result_uris)
        
    def test_integration1(self):
        self.__run_test((docs.example, docs.apple), 'example', ('http://example.com',))
