import sys
from freequery.document import Document
from freequery.repository.formats import WARCWriter

inpath = sys.argv[1]
outpath = inpath + '.warc'
infile = open(inpath, 'rb')
outfile = open(outpath, 'w+b')
warcwriter = WARCWriter(outfile)

WB_DELIM = "==P=>>>>=i===<<<<=T===>=A===<=!Junghoo!==>\n"

uri = None
raw = None
state = 'raw'
for line in infile:
    if state == 'raw':
        if line == WB_DELIM:
            if uri:
                doc = Document(uri, "".join(raw))
                warcwriter.write(doc)
            uri = None
            raw = []
            state = 'webbaseheaders'
        else:
            raw.append(line)
    elif state == 'webbaseheaders':
        if line.startswith('URL: '):
            uri = line[5:].strip()
        if line == "\r\n" or line == "\n":
            state = 'httpheaders'
    elif state == 'httpheaders':
        # dont index error or redirect responses
        if line.startswith('HTTP/1.1 30') or line.startswith('HTTP/1.1 4') or \
                line.startswith('HTTP/1.1 5'):
            uri = None
        if line == "\r\n" or line == "\n":
            state = 'raw'

outfile.close()
infile.close()
