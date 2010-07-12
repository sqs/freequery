import unittest
from freequery.lang import stemmer, stopwords, terms


class TestLang(unittest.TestCase):

    def test_stemmer(self):
        self.assertEquals('run', stemmer.stem_word('running'))
    
    def test_stopwords(self):
        self.assertTrue('the' in stopwords.stopwords)

    def test_prep_terms(self):
        ts = ['THE', 'Running']
        self.assertEquals(['run'], terms.prep_terms(ts))

    def test_prep_bad_terms(self):
        self.assertEquals(None, terms.prep_term(''))
        self.assertEquals(None, terms.prep_term('z'))

