import unittest
from freequery.lang import stemmer, stopwords, terms


class TestLang(unittest.TestCase):

    def test_stemmer(self):
        assert 'run' == stemmer.stem_word('running')
    
    def test_stopwords(self):
        assert 'the' in stopwords.stopwords

    def test_prep_terms(self):
        ts = ['THE', 'Running']
        assert ['run'] == terms.prep_terms(ts)

