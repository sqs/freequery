from freequery.test import IntegrationTestCase

class TestSmall1(IntegrationTestCase):
    dumps = ['small1']
    expected_results = {
        'welcom': ['http://example.com/'],
    }
    index = True
    rank = True
    niter = 5
    expected_ranking = ('http://example.com/',
                        'http://example.com/about',
                        'http://example.com/contact')
    check_against_local_pagerank = True
