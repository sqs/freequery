from freequery.test import IntegrationTestCase

class TestDuplicateURIs(IntegrationTestCase):
    dumps = ['small1']
    expected_results = {
        'welcom': ['http://example.com/'],
    }
    index = True
    rank = False
