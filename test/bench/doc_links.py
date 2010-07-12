import os
from freequery.test.benchmark import bench

from freequery.document import Document

path = os.path.join(os.path.dirname(__file__), 'large_sample_doc.html')
f = open(path, 'rb')
raw = f.read().decode('utf8')
f.close()

def newdoc():
    return Document('http://en.wikipedia.org/wiki/United_States', raw)

def run_gen(c):
    return lambda: list(c())

bench((#('links_bsoup', newdoc().links_bsoup),
      ('links_lxml_etree', run_gen(newdoc().links_lxml_html)),))
