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
                raise Exception("stopwords not yet supported in Query")
        stemmed_q = klass.stemmer_re.sub(stem_match, q)
        return discodb.Q.parse(stemmed_q)
