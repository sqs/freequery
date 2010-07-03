import os
from freequery.test.benchmark import bench

from freequery.document import Document

path = os.path.join(os.path.dirname(__file__), 'doc_links_sample_wikipedia_united_states.html')
f = open(path, 'rb')
raw = f.read()
f.close()
doc = Document('http://en.wikipedia.org/wiki/United_States', raw)

bench(2, (('link_uris_bsoup', doc.link_uris),))
