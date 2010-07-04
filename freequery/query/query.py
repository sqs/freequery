import re
import discodb
from freequery.lang.terms import prep_term

class Query(discodb.Q):
    stemmer_re = re.compile(r'[\w0-9.@:_-]+')
    @classmethod
    def parse(klass, q):
        def stem_match(m):
            t = prep_term(m.group(0))
            if t:
                return t
            else:
                # handle stopwords by making them equivalent to
                # (a | ~a) = True - this essentially removes them,
                # but without having to simplify the entire expression, which
                # would be much more complex.
                return "(a | ~a)"
        stemmed_q = klass.stemmer_re.sub(stem_match, q)
        return discodb.Q.parse(stemmed_q)
