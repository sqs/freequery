from freequery.test import IntegrationTestCase

class TestSmall(IntegrationTestCase):
    dumps = ['small1', 'small2']
    expected_results = {
        'welcom': ['http://example.com/'],
        'news': ['http://example.com/news'],
    }
    index = True
    rank = True
    niter = 2
    expected_ranking = ('http://example.com/',
                        'http://example.com/about',
                        'http://example.com/contact',
                        'http://example.com/news',
                        )

