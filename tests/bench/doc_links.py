import os, sys
from freequery.test.benchmark import bench

from freequery.document import Document

n = 20
if len(sys.argv) == 2:
    n = int(sys.argv[1])

path = os.path.join(os.path.dirname(__file__), 'doc_links_sample_wikipedia_united_states.html')
f = open(path, 'rb')
raw = f.read()
f.close()

def newdoc():
    return Document('http://en.wikipedia.org/wiki/United_States', raw)

def run_gen(c):
    return lambda: list(c())

bench(n, (#('links_bsoup', newdoc().links_bsoup),
          ('links_lxml_etree', run_gen(newdoc().links_lxml_html)),))
