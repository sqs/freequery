import re, urllib2, os, cPickle as pickle
from cStringIO import StringIO
from disco.ddfs import DDFS
from disco.util import urlresolve
from freequery.repository.formats import QTableFile

class DocumentNotFound(Exception): pass

class Docset(object):
    """
    A `Docset` represents a set of documents, contained in dump files stored on
    DDFS. Class instantiation alone doesn't do anything to DDFS; the DDFS tag
    for this docset won't exist until a dump is added.
    """

    def __init__(self, docset_name):
        self.ddfs_tag = docset_name
        self.ddfs_index_tag = docset_name + ':index'
        self.ddfs = DDFS()
        self.__index = None
        self.dirty = False

    def exists(self):
        """Returns True if this Docset exists in DDFS."""
        return self.ddfs.exists(self.ddfs_tag)
        
    def delete(self):
        """
        Deletes this tag from DDFS. DDFS garbage collection will soon take care
        of dumps in this docset with no other tags. If other docsets link to
        this docset's dumps, then those dumps will remain.
        """
        self.ddfs.delete(self.ddfs_index_tag)
        self.ddfs.delete(self.ddfs_tag)

    INDEX_VERSION_PAD = 4
    @property
    def index(self):
        # Lazily load index data from DDFS.
        if self.__index is None:
            blobs = [uri for (uri,) in self.ddfs.blobs(self.ddfs_index_tag)]
            if len(blobs) == 0:
                self.__index = {}
                self.__index_version = 0
            else:
                # Find blob with highest version number.
                ver, discouri = sorted([(self.__blob_uri_to_dump_name(uri), uri)
                                        for uri in blobs], reverse=True)[0]
                uri = urlresolve(discouri)
                data = urllib2.urlopen(uri).read()
                try:
                    self.__index = pickle.loads(data)
                    self.__index_version = int(ver)
                except EOFError:
                    raise EOFError("EOF reading docset index at %s in tag %s" % \
                                       (uri, self.ddfs_index_tag))
        return self.__index

    def save(self):
        self.index # load if hasn't been loaded yet
        self.__index_version += 1
        ver = "%0*d" % (self.INDEX_VERSION_PAD, self.__index_version)
        tmp_fname = os.path.join("/tmp/", "%s%s" % (self.ddfs_index_tag, ver))
        with open(tmp_fname, 'r+b') as f:
            pickle.dump(self.__index, f)
            f.flush()
            f.seek(0)
            self.ddfs.push(self.ddfs_index_tag, [(f, ver)])
        self.dirty = False

    def add_dump(self, dumpname, dump):
        """
        Adds a dump to this docset and indexes its documents by position,
        appending the doc count to the name of the dump and then uploading the
        dump to DDFS with the tag for this docset.
        """
        # index positions
        startpos = 0
        endpos = None
        with open(dump, 'rb') as f:
            dociter = QTableFile(f)
            for doc in dociter:
                endpos = dociter.tell()
                self.index[doc.uri] = (dumpname, startpos, endpos - startpos)
                startpos = endpos
        self.ddfs.push(self.ddfs_tag, [(dump, dumpname)])
        self.dirty = True

    @property
    def doc_count(self):
        """
        Returns the total number of documents contained in all dumps in this
        docset.
        """
        return len(self.index)

    def doc_uris(self):
        """Returns all URIs of documents contained in all dumps in this
        docset."""
        return self.index.keys()
    
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
        """Returns the names of dumps in the docset."""
        return [self.__blob_uri_to_dump_name(uri) for uri in self.dump_uris()]

    def get_pos(self, uri):
        """Returns a tuple `(dump_name, byte pos)` of the location of the
        document `uri` in the docset."""
        if uri in self.index:
            return self.index[uri]
        else:
            raise DocumentNotFound()
    
    def get(self, uri):
        """Returns the `Document` with the specified `uri`."""
        for dump_uri in self.dump_uris():
            f = urllib2.urlopen(urlresolve(dump_uri))
            for doc in QTableFile(f):
                if doc.uri == uri:
                    return doc
        raise DocumentNotFound()
