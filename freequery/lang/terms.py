from freequery.lang import stemmer
from freequery.lang.stopwords import stopwords


def prep_terms(terms):
    """
    Returns a list of terms derived from `terms` with stopwords removed
    and other modifications.
    """
    return filter(bool, map(prep_term, [t.lower() for t in terms]))

def prep_terms_unique(terms):
    """
    Like prep_terms, but assumes that positional information doesn't matter,
    so is faster.
    """
    return filter(bool, stemmer.stem_words(t for t in set(t.lower() for t in terms) if len(t) > 1 and t not in stopwords))

def prep_term(t):
    if len(t) <= 1:
        return None
    if t in stopwords:
        return None
    return stemmer.stem_word(t)
