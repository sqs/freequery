import re
from disco.ddfs import DDFS

class Docset(object):

    def __init__(self, name):
        self.name = name
        self.ddfs = DDFS()

    def add(self, dumpname, dump):
        return self.ddfs.push(self.name, [(dump, dumpname)])

    def dump_uris(self):
        return (uri for (uri,) in self.ddfs.blobs(self.name))
    
    def __blob_uri_to_dump_name(self, bloburi):
        """
        Takes a blob URI like
           disco://host/ddfs/vol0/blob/b4/dumpname1$4fd-ea750-6d4e1
        and returns "dumpname".
        """
        return re.search(r'/([\w0-9_\-@:]+)\$', bloburi).group(1)
    
    def dump_names(self):
        return [self.__blob_uri_to_dump_name(uri) for uri in self.dump_uris()]

    
    
