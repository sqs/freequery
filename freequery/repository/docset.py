import re
from disco.ddfs import DDFS
from freequery.repository.formats import QTableFile

class Docset(object):

    def __init__(self, docset_name):
        self.ddfs_tag = docset_name
        self.ddfs = DDFS()

    def exists(self):
        return self.ddfs.exists(self.ddfs_tag)
        
    def delete(self):
        return self.ddfs.delete(self.ddfs_tag)

    NDOCS_SUFFIX = '_ndocs'
    NDOCS_RE = re.compile(r'^(?P<name>[\w\d.:_\-]+)_ndocs(?P<ndocs>\d+)$')
    def add_dump(self, dumpname, dump):
        if self.NDOCS_SUFFIX not in dumpname:
            dumpname += "%s%d" % \
                (self.NDOCS_SUFFIX, self.__doc_count_in_dump(dump))
        return self.ddfs.push(self.ddfs_tag, [(dump, dumpname)])

    def doc_count(self):
        return sum(int(self.NDOCS_RE.match(s).group('ndocs')) \
                       for s in self.dump_names())

    def __doc_count_in_dump(self, dump):
        with open(dump, 'rb') as f:
            return sum(1 for doc in QTableFile(f))

    def dump_uris(self):
        return (uri for (uri,) in self.ddfs.blobs(self.ddfs_tag))
    
    def __blob_uri_to_dump_name(self, bloburi):
        """
        Takes a blob URI like
           disco://host/ddfs/vol0/blob/b4/dumpname1$4fd-ea750-6d4e1
        and returns "dumpname".
        """
        return re.search(r'/([\w0-9_\-@:]+)\$', bloburi).group(1)
    
    def dump_names(self):
        return [self.__blob_uri_to_dump_name(uri) for uri in self.dump_uris()]

    def dump_names_without_doc_counts(self):
        return [self.NDOCS_RE.match(s).group('name') for s in self.dump_names()]
    
