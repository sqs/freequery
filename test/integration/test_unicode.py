from freequery.test import IntegrationTestCase

class TestUnicode(IntegrationTestCase):
    dumps = ['small5-chinese', 'unicode-test']
    expected_results = {

    }
    index = True
    rank = True
