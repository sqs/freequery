import string
from freequery.lang import stemmer
from freequery.lang.stopwords import stopwords

def prep_terms(terms):
    """
    Returns a list of terms derived from `terms` with stopwords removed
    and other modifications.
    """
    return filter(bool, map(prep_term, terms))

def prep_term(t):
    if len(t) <= 1:
        return None
    assert t[0] not in string.whitespace and t[-1] not in string.whitespace
    t = t.lower()
    if t in stopwords:
        return None
    return stemmer.stem_word(t)
