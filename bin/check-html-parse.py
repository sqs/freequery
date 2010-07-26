import sys
from freequery.formats.warc import WARCParser

inpaths = sys.argv[1:]

for path in inpaths:
    print "@ %s" % path
    for doc in WARCParser(open(path, 'rb')):
        print doc.uri
        doc.html_parser
        #doc.links_lxml_html()
        #for uri in doc.link_uris:
        #    pass#print " - %s" % uri
