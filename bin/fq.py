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
    
@Freequery.command
def query(program, index, q):
    """Usage: <index> <query>

    Query the inverted index for docs matching `query`.
    """
    import discodb
    index = "discodex:fq:%s:invindex" % index
    q = discodb.Q.parse(q)
    print "\n".join(program.discodex_client.query(index, q))

@Freequery.command
def index(program, docsetname):
    """Usage: <docsetname>

    Indexes the specified docset.
    """
    import sys, time
    from discodex.objects import DataSet
    from freequery.repository.docset import Docset
    docset = Docset(docsetname)
    if not docset.exists():
        print "fq: cannot index `%s': no such docset" % docsetname
        exit(1)
    from disco.util import urlresolve
    dataset = DataSet(input=map(urlresolve, list(docset.dump_uris())),
                      options=dict(parser='freequery.index.mapreduce.docparse',
                                   demuxer='freequery.index.mapreduce.docdemux'))
    orig_spec = program.discodex_client.index(dataset)
    if orig_spec:
        print "indexing: %s " % orig_spec,
    else:
        print "fq: discodex failed to index `%s'" % docsetname
        exit(2)
        
    # wait for indexing to complete
    while True:
        try:
            program.discodex_client.get(orig_spec)
            break
        except:
            time.sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()
    spec = "fq:%s:invindex" % docsetname
    program.discodex_client.clone(orig_spec, spec)
    print "\n", spec

@Freequery.command
def inspect_index(program, index):
    import simplejson, urllib2
    index = "discodex:fq:%s:invindex" % index
    r = urllib2.urlopen("http://localhost:8080/indices/%s/items" % index).read()
    for k,v in simplejson.loads(r):
        print "'%s': %r" % (k,v)
    
if __name__ == '__main__':
    Freequery(option_parser=FreequeryOptionParser()).main()
