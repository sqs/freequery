from freequery.document import Document

example = Document('http://example.com', '<h1>Welcome to example</h1>')
apple = Document('http://apple.com', '<h1>Welcome to Apple</h1>')
stanford = Document('http://stanford.edu', '<h1>Stanford</h1>' \
                    '<p><a href="http://cs.stanford.edu">' \
                    'Stanford Computer Science</a></p>')
examplez = Document('http://example.com/z.html', '<h1>Example z</h1>')

all_docs = [example, apple, stanford]
for doc in all_docs:
    doc.make_typed('text/html')

warc_file1 = """WARC/0.18
WARC-Type: response
WARC-Target-URI: http://example.com
Content-Length: 31



<h1>Welcome to example</h1>

WARC/0.18
WARC-Type: response
WARC-Target-URI: http://apple.com
Content-Length: 29



<h1>Welcome to Apple</h1>

"""

warc_file2 = """WARC/0.18
WARC-Type: response
WARC-Target-URI: http://example.com/m.html
Content-Length: 22



<h1>Example m</h1>

WARC/0.18
WARC-Type: response
WARC-Target-URI: http://example.com/z.html
Content-Length: 22



<h1>Example z</h1>

"""

def dumppath(dumpname):
    import os
    return os.path.join(os.path.dirname(__file__),
                        '../../test/dumps/', dumpname)

def dumpdocs(dumpname):
    from freequery.formats.warc import WARCParser
    return dict((doc.uri, doc) for doc in WARCParser(open(dumppath(dumpname), 'rb')))
