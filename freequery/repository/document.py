import re

class Document(object):

    """
    Represents a document.
    """

    def __init__(self, uri, raw):
        self.uri = uri
        self.raw = raw

    def terms(self):
        raise NotImplementedError

    def make_typed(self, mimetype):
        self.__class__ = MIMETYPE_CLASS[mimetype]
        return self
    
    def __eq__(self, other):
        return isinstance(other, Document) and self.__dict__ == other.__dict__
    
    def __str__(self):
        return "<Document uri='%s'>" % self.uri


class HTMLDocument(Document):

    strip_tags_re = re.compile(r'<[^>]+>')
    collapse_space_re = re.compile(r'\s+')
    alphanum_re = re.compile(r'[^a-z0-9]+')
    
    def term_hits(self):
        html = self.raw
        txt = re.sub(self.strip_tags_re, ' ', html)
        txt = txt.lower().strip()
        txt = re.sub(self.alphanum_re, ' ', txt)
        txt = re.sub(self.collapse_space_re, ' ', txt)
                
        pos = 0
        term_hits = {}
        for term in txt.split(' '):
            if term not in term_hits:
                term_hits[term] = []
            hit = Hit(pos)
            term_hits[term].append(hit)
            pos += 1
        return term_hits
        

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

