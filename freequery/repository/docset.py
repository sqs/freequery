import re, urllib2
from disco.ddfs import DDFS
from disco.util import urlresolve
from freequery.repository.formats import QTableFile

class Docset(object):
    """
    A `Docset` represents a set of documents, contained in dump files stored on
    DDFS. Class instantiation alone doesn't do anything to DDFS; the DDFS tag
    for this docset won't exist until a dump is added.
    """

    def __init__(self, docset_name):
        self.ddfs_tag = docset_name
        self.ddfs = DDFS()
        self.index = {}

    def exists(self):
        """Returns True if this Docset exists in DDFS."""
        return self.ddfs.exists(self.ddfs_tag)
        
    def delete(self):
        """
        Deletes this tag from DDFS. DDFS garbage collection will soon take care
        of dumps in this docset with no other tags. If other docsets link to
        this docset's dumps, then those dumps will remain.
        """
        self.ddfs.delete(self.ddfs_tag)

    NDOCS_SUFFIX = '_ndocs'
    NDOCS_RE = re.compile(r'^(?P<name>[\w\d.:_\-]+)_ndocs(?P<ndocs>\d+)$')
    def add_dump(self, dumpname, dump):
        """
        Adds a dump to this docset and indexes its documents by position,
        appending the doc count to the name of the dump and then uploading the
        dump to DDFS with the tag for this docset.
        """
        # index positions
        doc_count = 0
        startpos = 0
        endpos = None
        with open(dump, 'rb') as f:
            dociter = QTableFile(f)
            for doc in dociter:
                doc_count += 1
                endpos = dociter.tell()
                self.index[doc.uri] = (dumpname, startpos, endpos - startpos)
                startpos = endpos
            
        if self.NDOCS_SUFFIX not in dumpname:
            dumpname += "%s%d" % (self.NDOCS_SUFFIX, doc_count)
        return self.ddfs.push(self.ddfs_tag, [(dump, dumpname)])

    def doc_count(self):
        """
        Returns the total number of documents contained in all dumps in this
        docset.
        """
        return sum(int(self.NDOCS_RE.match(s).group('ndocs')) \
                       for s in self.dump_names())

    def dump_uris(self):
        """
        Returns disco:// URIs for each dump in the docset. Use
        disco.util.urlresolve to convert the disco:// URIs to http:// URIs.
        """
        return (uri for (uri,) in self.ddfs.blobs(self.ddfs_tag))
    
    def __blob_uri_to_dump_name(self, bloburi):
        """
        Takes a blob URI like
           disco://host/ddfs/vol0/blob/b4/dumpname1$4fd-ea750-6d4e1
        and returns "dumpname".
        """
        return re.search(r'/([\w0-9_\-@:]+)\$', bloburi).group(1)
    
    def dump_names(self):
        """Returns the names, including doc counts, of dumps in the docset."""
        return [self.__blob_uri_to_dump_name(uri) for uri in self.dump_uris()]

    def dump_names_without_doc_counts(self):
        """Returns the names, without doc counts, of dumps in the docset."""
        return [self.NDOCS_RE.match(s).group('name') for s in self.dump_names()]

    def get_pos(self, uri):
        """Returns a tuple `(dump_name, byte pos)` of the location of the
        document `uri` in the docset."""
        return self.index[uri]
    
    def get(self, uri):
        """Returns the `Document` with the specified `uri`."""
        for dump_uri in self.dump_uris():
            f = urllib2.urlopen(urlresolve(dump_uri))
            for doc in QTableFile(f):
                if doc.uri == uri:
                    return doc
        raise KeyError
