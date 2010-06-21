import re
from freequery.lang.terms import prep_terms

class Document(object):

    """
    Represents a document.
    """

    def __init__(self, uri, raw, docid=-1):
        self.uri = uri
        self.raw = raw
        self.docid = docid
        self.make_typed('text/html')

    def terms(self):
        raise NotImplementedError

    def make_typed(self, mimetype):
        self.__class__ = MIMETYPE_CLASS[mimetype]
        return self

    def tokens(self):
        return NotImplementedError

    def terms(self):
        return prep_terms(self.tokens())

    def term_frequencies(self):
        tfs = dict()
        for term in self.terms():
            if term in tfs:
                tfs[term] += 1
            else:
                tfs[term] = 1
        return tfs
    
    def term_hits(self):
        pos = 0
        term_hits = {}
        for term in self.terms():
            if term not in term_hits:
                term_hits[term] = []
            hit = Hit(pos)
            term_hits[term].append(hit)
            pos += 1
        return term_hits
    
    def __eq__(self, other):
        return isinstance(other, Document) and self.__dict__ == other.__dict__
    
    def __str__(self):
        return "<Document docid=%d uri='%s' raw=(%d bytes)>" % (self.docid, self.uri, len(self.raw))

    __unicode__ = __str__
    __repr__ = __str__


class HTMLDocument(Document):

    strip_tags_re = re.compile(r'<[^>]+>')
    collapse_space_re = re.compile(r'\s+')
    alphanum_re = re.compile(r'[^\w\d]+')
    
    def tokens(self):
        html = self.raw
        txt = re.sub(self.strip_tags_re, ' ', html)
        txt = txt.strip()
        txt = re.sub(self.alphanum_re, ' ', txt)
        txt = re.sub(self.collapse_space_re, ' ', txt)
        return txt.split(' ')
                
        
class Hit(object):
    """
    Represents an occurrence of a term in a document.
    """

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return "<Hit pos=%d>" % self.pos


MIMETYPE_CLASS = {
    'text/html': HTMLDocument
}


