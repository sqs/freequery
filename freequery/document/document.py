import urlparse
from cStringIO import StringIO
import lxml.html
from freequery.lang.terms import prep_terms

class Document(object):

    """
    Represents a document.
    """

    def __init__(self, uri, raw=None, docid=-1):
        self.uri = uri
        self.raw = raw
        self.docid = docid
        self.make_typed('text/html')

        self.__cached_link_uris = None

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

    @property
    def link_uris(self):
        """Returns absolute URIs of all links in the document."""
        if self.__cached_link_uris is not None:
            return self.__cached_link_uris
        else:
            return [link.dest_uri for link in self.links()]

    def cache_link_uris(self, link_uris):
        self.__cached_link_uris = link_uris
    
    def __eq__(self, other):
        return isinstance(other, Document) and self.uri == other.uri and \
            self.raw == other.raw and self.docid == other.docid
    
    def __str__(self):
        return "<Document docid=%d uri='%s' raw=%d>" % (self.docid, self.uri, bool(self.raw))

    __unicode__ = __str__
    __repr__ = __str__


class HTMLDocument(Document):

    @property
    def html_parser_lxml_html(self):
        if self.__html_parser_lxml_html is None:
            if self.raw is None:
                raise Exception("can't parse HTML with raw=None")
            self.__html_parser_lxml_html = lxml.html.fromstring(self.raw, base_url=self.uri)
        return self.__html_parser_lxml_html
    __html_parser_lxml_html = None
    
    html_parser = html_parser_lxml_html

    @property
    def title(self):
        return self.html_parser.xpath('.//title')[0].text

    def tokens(self):
        return [w for w in self.html_parser.text_content().split() \
                    if w.isalnum()]

    def links_lxml_html(self):
        self.html_parser.make_links_absolute(self.uri, resolve_base_href=True)
        for e,attr,uri,pos in self.html_parser.iterlinks():
            tag = e.tag
            if tag == "a" or tag == "A":
                yield Link(uri)

    links = links_lxml_html

    def excerpt(self, qq, radius=175):
        """
        Returns a textual excerpt of the document for the
        :class:`freequery.query.Query` `qq`.
        """
        txt = self.html_parser.text_content()
        txt_lower = txt.lower()
        for term in qq.non_negated_literals():
            i = txt_lower.find(term)
            if i != -1:
                startpos = max(i - radius, 0)
                # Want full term in excerpt, even if it's longer than radius.
                # TODO: This compensates by the length of the stemmed term in
                # the query, not by the length of the actual term in the doc.
                endpos = min(i + len(term) + radius, len(txt))

                # Add '...' if truncated at start or end.
                if startpos != 0:
                    startmarker = '...'
                else:
                    startmarker = ''
                if endpos != len(txt):
                    endmarker = '...'
                else:
                    endmarker = ''
                return startmarker + txt[startpos:endpos] + endmarker
                
        raise Exception("couldn't make excerpt for doc '%s' txt='%s' with lits=%r" % \
                            (self.uri, txt, qq.non_negated_literals()))
        
class Hit(object):
    """
    Represents an occurrence of a term in a document.
    """

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return "<Hit pos=%d>" % self.pos

class Link(object):
    """
    Represents a link in a document.
    """

    def __init__(self, dest_uri, attrs=None):
        self.dest_uri = dest_uri
        self.attrs = attrs

    def __str__(self):
        return "<Link to='%s' attrs=%r>" % (self.dest_uri, self.attrs)
    

MIMETYPE_CLASS = {
    'text/html': HTMLDocument
}


