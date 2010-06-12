import re, struct

class Document(object):

    """
    Represents a document.
    """

    def __init__(self, uri, raw, docid=-1):
        self.uri = uri
        self.raw = raw
        self.docid = docid

    def terms(self):
        raise NotImplementedError

    def make_typed(self, mimetype):
        self.__class__ = MIMETYPE_CLASS[mimetype]
        return self

    doc_struct = struct.Struct('i255p255p')
    def pack(self):
        return self.doc_struct.pack(self.docid, self.uri, self.raw)
    
    @classmethod
    def unpack(klass, s):
        docid, uri, raw = klass.doc_struct.unpack(s)
        return klass(uri, raw, docid)

    @classmethod
    def unpack_from_file(klass, file):
        buffer = file.read(klass.doc_struct.size)
        docid, uri, raw = klass.doc_struct.unpack_from(buffer)
        return klass(uri, raw, docid)
    
    def __eq__(self, other):
        return isinstance(other, Document) and self.__dict__ == other.__dict__
    
    def __str__(self):
        return "<Document docid=%d uri='%s'>" % (self.docid, self.uri)


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

