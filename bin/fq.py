#!/usr/bin/env python

import os, sys

from clx import OptionParser, Program

class FreequeryOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

class Freequery(Program):
    @property
    def option_dict(self):
        return dict((k, v) for k, v in self.options.__dict__.iteritems()
                           if v is not None)

    @property
    def discodex_client(self):
        from discodex.client import DiscodexClient
        return DiscodexClient()

    @property
    def fqclient(self):
        from freequery.client import FreequeryClient
        return FreequeryClient
    
@Freequery.command
def query(program, spec, q):
    """Usage: <spec> <query>

    Query the `spec` inverted index for docs matching `query`.
    """
    for i,doc in enumerate(program.fqclient(spec).query(q)):
        print "%d. %s" % (i+1, doc.uri)

@Freequery.command
def index(program, spec):
    """Usage: <spec>

    Indexes the specified docset.
    """
    import sys, time
    from discodex.objects import DataSet
    from freequery.repository.docset import Docset
    from freequery.client.client import Spec
    spec = Spec(spec)
    docset = Docset(spec.docset_name)
    if not docset.exists():
        print "fq: cannot index `%s': no such docset" % spec.docset_name
        exit(1)
    from disco.util import urlresolve
    dataset = DataSet(input=map(urlresolve, list(docset.dump_uris())),
                      options=dict(parser='freequery.index.mapreduce.docparse',
                                   demuxer='freequery.index.mapreduce.docdemux'))
    orig_invindex_name = program.discodex_client.index(dataset)
    if orig_invindex_name:
        print "indexing: %s " % orig_invindex_name,
    else:
        print "fq: discodex failed to index `%s'" % spec.name
        exit(2)
        
    # wait for indexing to complete
    while True:
        try:
            program.discodex_client.get(orig_invindex_name)
            break
        except:
            time.sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()
    program.discodex_client.clone(orig_invindex_name, spec.invindex_name)
    print "\n", spec.invindex_name

@Freequery.command
def inspect_index(program, soec):
    import simplejson, urllib2
    from freequery.client.client import Spec
    invindex_name = Spec(spec).invindex_name
    r = urllib2.urlopen("http://localhost:8080/indices/%s/items" %\
                            invindex_name).read()
    for k,v in simplejson.loads(r):
        print "'%s': %r" % (k,v)

@Freequery.command
def rank(program, spec):
    from freequery.repository.docset import Docset
    from freequery.graph.pagerank import PagerankJob
    from freequery.client.client import Spec
    spec = Spec(spec)
    docset = Docset(spec.docset_name)
    job = PagerankJob(docset)
    job.start()

    show_scores(program, spec.name)

@Freequery.command
def show_scores(program, spec):
    """Usage: <spec>

    Shows the scores of documents in the specified `spec` ScoreDB file.
    """
    from freequery.graph.scoredb import ScoreDB
    from freequery.client.client import Spec
    spec = Spec(spec)
    scoredb = ScoreDB(spec.scoredb_path)
    for uri, score in scoredb.items():
        print "%.8f\t%s" % (score, uri)
    
if __name__ == '__main__':
    Freequery(option_parser=FreequeryOptionParser()).main()
