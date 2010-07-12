"""
Parsers and writers for Web page dump files.
"""
from freequery.document import Document

class WARCFormatError(Exception): pass

class WARCParser(object):

    """Parser for WARC files."""

    def __init__(self, stream):
        self.pos = 0
        if isinstance(stream, str) or isinstance(stream, unicode):
            from StringIO import StringIO
            stream = StringIO(stream)
        self.stream = stream

    def tell(self):
        """Returns the cursor position (in bytes) in `iterable`. Used for the
        :class:`Docset` index."""
        return self.pos

    def __parse_header_line(self, line):
        k,v = line.split(":", 1)
        v = v.strip()
        return (k,v)
    
    def next(self):
        # version
        version = self.stream.readline()
        self.pos += len(version)
        if version == '':
            raise StopIteration
        if not version.startswith('WARC/'):
            raise WARCFormatError("record does not start with `version`:" \
                                  " '%s' at pos %d" % (version, self.pos))

        # record header
        warc_type = None
        warc_target_uri = None
        content_length = None
        while True:
            line = self.stream.readline()
            self.pos += len(line)
            if line == "\n":
                break
            else:
                k,v = self.__parse_header_line(line)
                if k == 'WARC-Type':
                    warc_type = v
                elif k == 'WARC-Target-URI':
                    warc_target_uri = v.decode('utf8')
                elif k == 'Content-Length':
                    content_length = int(v)

        # check some required fields
        if warc_type is None:
            raise WARCFormatError("WARC-Type is required")
        if warc_type == 'response' and warc_target_uri is None:
            raise WARCFormatError("WARC-Target-URI is required")
        if content_length is None:
            raise WARCFormatError("Content-Length is required")
                
        # block
        block = self.stream.read(content_length)
        self.pos += content_length        
        
        # remove "\n" from last line of raw, since it delimits
        # the raw from the end-of-document and is not actually part
        # of the raw content
        ##if len(raw) > 0:
        ##    raw[-1] = raw[-1].rstrip()

        if warc_type == 'response':
            # skip response headers
            raw = block[block.index("\n\n")+len("\n\n"):-len("\n\n")]
            return Document(warc_target_uri, raw)
        else:
            return self.next()

    def __iter__(self):
        return self

    
class WARCWriter(object):

    """Writer for WARC files."""
    
    def __init__(self, out):
        self.out = out

    def write(self, doc):
        """Writes `doc` to the output stream."""
        self.out.writelines((doc.uri.encode('utf8'), "\n\n",
                             doc.raw.encode('utf8'), "\n"))

    
