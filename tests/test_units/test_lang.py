import unittest
from freequery.lang import stemmer, stopwords


class TestLang(unittest.TestCase):

    def test_stemmer(self):
        assert 'run' == stemmer.stem_word('running')
    
    def test_stopwords(self):
        assert 'the' in stopwords.stopwords

