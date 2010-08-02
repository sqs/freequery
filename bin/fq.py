#!/usr/bin/env python

import os, sys

from clx import OptionParser, Program

class FreequeryOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)
        self.add_option('-u', '--unranked',
                        action='store_true',
                        help='return unranked query results')
        self.add_option('-p', '--profile',
                        action='store_true',
                        help='show profiler stats for Disco jobs')


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
    """Usage: [--unranked] <spec> <query>

    Query the `spec` inverted index for docs matching `query`.
    """
    unranked = program.option_dict.get('unranked', False)
    res = program.fqclient(spec).query(q, ranked=not unranked)
    if not unranked:
        res.sort(reverse=True)
    for i,doc in enumerate(res):
        print "%d. %s %r" % (i+1, doc.uri, doc.score)
        print "\t%s\n" % doc.excerpt.replace("\n", " ")

@Freequery.command
def index(program, spec):
    """Usage: <spec>

    Indexes the specified docset.
    """
    import sys, time
    from freequery.client.client import Spec
    program.fqclient(spec).index()

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
    from freequery.client.client import Spec
    program.fqclient(spec).rank(profile=program.option_dict.get('profile', False))

@Freequery.command
def show_scores(program, spec):
    """Usage: <spec>

    Shows the scores of documents in the specified `spec` ScoreDB file.
    """
    from freequery.index.scoredb import ScoreDB
    from freequery.client.client import Spec
    spec = Spec(spec)
    scoredb = ScoreDB(spec.scoredb_path)
    for uri, score in scoredb.items():
        print "%.8f\t%s" % (score, uri)

@Freequery.command
def dump_lint(program, *dumps):
    """Usage: <dump1> <dump2> ...

    Checks the validity of the specified dump file:
      - No two documents have the same URI.
    """
    from freequery.formats.warc import WARCParser
    from collections import defaultdict
    uri_dump = defaultdict(list)
    for dump in dumps:
        with open(dump, 'rb') as f:
            for doc in WARCParser(f):
                uri_dump[doc.uri].append(dump)
    ok = True
    for uri,dumps in uri_dump.items():
        if len(dumps) > 1:
            print "*** Duplicate URI '%s' in: " % uri
            for dump in dumps:
                print "    - %s" % dump
            ok = False
    if ok:
        print "OK"
    
if __name__ == '__main__':
    Freequery(option_parser=FreequeryOptionParser()).main()
