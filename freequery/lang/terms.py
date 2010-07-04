from freequery.lang import stemmer
from freequery.lang.stopwords import stopwords


def prep_terms(terms):
    """
    Returns a list of terms derived from `terms` with stopwords removed
    and other modifications.
    """
    terms = [t.lower() for t in terms if len(t) > 1]
    terms = [t for t in terms if t not in stopwords]
    return filter(bool, stemmer.stem_words(terms))

def prep_term(t):
    t = prep_terms([t])
    if len(t) == 1:
        return t[0]
