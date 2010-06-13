import re, struct
from freequery.repository.repository_pb2 import Document as proto_Document
from freequery.lang.terms import prep_terms

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

    size_header = struct.Struct('I')
    
    def to_proto(self):
        proto_doc = proto_Document()
        proto_doc.docid = self.docid
        proto_doc.uri = self.uri.decode('utf8')
        proto_doc.raw = self.raw.decode('utf8')
        return proto_doc
        
    def to_proto_string(self):
        proto_doc = self.to_proto()
        size = proto_doc.ByteSize()
        return self.size_header.pack(size) + proto_doc.SerializeToString()

    @classmethod
    def from_proto(klass, proto_doc):
        return klass(proto_doc.uri, proto_doc.raw, proto_doc.docid)

    @classmethod
    def from_proto_string(klass, s):
        """
        Read string `s` to parse a protobuf Document. See `from_proto_file`.
        """
        size = klass.size_header.unpack(s[:klass.size_header.size])[0]
        data = s[klass.size_header.size:]
        proto_doc = proto_Document()
        proto_doc.ParseFromString(data)
        return klass.from_proto(proto_doc)
    
    @classmethod
    def from_proto_file(klass, file):
        """
        Read `file` to parse a protobuf Document. The first sizeof(int) bytes are
        unsigned int `size`; the next `size` bytes are the serialized data.
        """
        try:
            size = klass.size_header.unpack(file.read(klass.size_header.size))[0]
        except:
            raise EOFError
        data = file.read(size)
        proto_doc = proto_Document()
        proto_doc.ParseFromString(data)
        return klass.from_proto(proto_doc)

    def tokens(self):
        return NotImplementedError
    
    def term_hits(self):
        pos = 0
        term_hits = {}
        terms = prep_terms(self.tokens())
        for term in terms:
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


