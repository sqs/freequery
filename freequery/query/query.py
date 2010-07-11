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
        qq = discodb.Q.parse(stemmed_q)
        qq.__class__ = klass
        return qq

    def non_negated_literals(self):
        """
        Returns all literals in the query that are not negated.
        """
        # TODO: should this preserve order of literals?
        lits = [item for sublist in [cl.literals for cl in self.clauses] for item in sublist]
        return [lit.term for lit in lits if not lit.negated]
