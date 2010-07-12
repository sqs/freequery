from disco.core import Disco, result_iterator
from freequery.repository.docset import Docset


class LinkParseJob(object):

    def __init__(self, spec, verbose=False, **kwargs):
        self.spec = spec
        self.docset = Docset(self.spec.docset_name)
        self.disco = Disco("disco://localhost")
        self.verbose = verbose

    def start(self):
        from freequery.index.mapreduce import docparse
        from disco import func
        job = self.disco.new_job(
            name="linkparse",
            input=self.docset.dump_uris(),
            map_reader=docparse,
            map=linkparse_map,
            map_output_stream=(func.map_output_stream,
                               func.disco_output_stream,
                               LinkFileOutputStream.disco_output_stream),
            partitions=0,
            save=True,
        )
        results = job.wait()

        if self.verbose:
            self.__print_results(results)

    def __print_results(self, results):
        for k,v in result_iterator(results, reader=doclinksparse):
            print "%s\n\t%s" % (k,"\n\t".join(v))
            

def linkparse_map(doc, params):
    yield doc.uri.encode('utf8'), [uri.encode('utf8') for uri in doc.link_uris()]

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


class LinkFileOutputStream(object):

    """Writer for link files."""
    
    def __init__(self, out):
        if out is None:
            raise Exception("LinkFileOutputStream out can't be None")
        self.out = out

    @staticmethod
    def disco_output_stream(stream, partition, url, params):
        from freequery.graph.links import LinkFileOutputStream
        return (LinkFileOutputStream(stream), None)

    def add(self, doc_uri, link_uris):
        """Writes data for `doc` and its links to the output stream."""
        self.write(doc_uri.encode('utf8') + "\n")
        for link_uri in link_uris:
            self.write(link_uri + "\n")
        self.write("\n")
    
    def write(self, data):
        self.out.write(data)
