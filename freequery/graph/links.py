def doclinksparse(iterable, size, fname, params):
    from freequery.graph.links import LinkFile
    return LinkFile(iterable)

def doclinkdemux(doc, params):
    """
    Emits `(doc_uri, (link_destination_uri, ...))` for each link
    in `doc`.
    """
    for link_uri in set(doc.link_uris()):
        yield doc.uri, link_uri

def doclinks(doc, params):
    yield doc.uri, list(doc.link_uris())

class LinkFile(object):

    """Parses a link file and yields (uri, (link1, link2, ...)) when iterated."""

    def __init__(self, iterable):
        if isinstance(iterable, file):
            self.iterable = iterable.__iter__()
        elif hasattr(iterable, 'read'):
            # disco.comm.Connection objects are iterator-like, but they don't
            # define __iter__ or next(), so just read in the whole
            # buffer. TODO: submit a patch to disco to have Connection expose
            # an iterator interface.
            self.iterable = iter(iterable.read().splitlines(True))
        elif isinstance(iterable, list):
            self.iterable = iter(iterable)

    def next(self):
        # doc URI
        uri = self.iterable.next().strip().decode('utf8')
        
        # links
        links = []
        for line in self.iterable:
            if line == "\n":
                break
            else:
                links.append(line.strip().decode('utf8'))

        return (uri, links)

    def __iter__(self):
        return self


class LinkFileWriter(object):

    """Writer for link files."""
    
    def __init__(self, out):
        self.out = out

    def write(self, doc):
        """Writes data for `doc` and its links to the output stream."""
        self.out.write(doc.uri.encode('utf8') + "\n")
        for link_uri in doc.link_uris():
            self.out.write(link_uri + "\n")
        self.out.write("\n")
