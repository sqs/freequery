#!/usr/bin/env python

import os, sys

from clx import OptionParser, Program

class FreequeryDocsetOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

        
class FreequeryDocset(Program):
    @property
    def option_dict(self):
        return dict((k, v) for k, v in self.options.__dict__.iteritems()
                           if v is not None)

    @property
    def ddfs(self):
        from disco.ddfs import DDFS
        return DDFS()

    @property
    def fqclient(self):
        from freequery.client.client import FreequeryClient
        return FreequeryClient

    @property
    def docset(self):
        from freequery.repository.docset import Docset
        return Docset
    
    def default(self, program, *args):
        ls(program)

@FreequeryDocset.command
def ls(program, spec=None):
    """Usage: [spec]

    Prints the names of all docsets, or of the dumps in the specified docset.
    """
    from freequery.client.client import Spec
    if spec is None:
        docsets = program.ddfs.list(Spec.docset_prefix)
        if docsets:
            print "\n".join(docsets)
    else:
        docset_name = Spec(spec).docset_name
        docset = program.docset(docset_name)
        if docset.exists():
            dumps = docset.dump_names()
            if dumps:
                print "\n".join(dumps)
        else:
            print "fq-docset: cannot access `%s': no such docset" % docset_name
            exit(1)

@FreequeryDocset.command
def rm(program, docsetname):
    """Usage: <spec>

    Deletes the specified docset.
    """
    from freequery.client.client import Spec
    docset_name = Spec(spec).docset_name
    docset = program.docset(docset_name)
    if docset.exists():
        program.docset(docset_name).delete()
    else:
        print "fq-docset: cannot remove `%s': no such docset" % docset_name
        exit(1)

@FreequeryDocset.command
def add(program, spec, *dumps):
    """Usage: <docsetname> <dump>

    Adds the dumpfile `dump` to the specified docset.
    """
    from freequery.client.client import Spec
    spec = Spec(spec)
    docset = program.docset(spec.docset_name)
    for dump in dumps:
        dumpname = os.path.basename(dump)
        docset.add_dump(dumpname, dump)
    docset.save()

@FreequeryDocset.command
def info(program, spec):
    """Usage: <spec>

    Prints info about the specified docset.
    """
    from freequery.client.client import Spec
    spec = Spec(spec)
    docset = program.docset(spec.docset_name)
    print "Docset '%s'" % spec.docset_name
    print "Number of documents: %d" % docset.doc_count
    print "Dumps:"
    for i,dump_name in enumerate(docset.dump_names()):
        print "  %d. %s" % (i+1, dump_name)

@FreequeryDocset.command
def linkparse(program, spec):
    """Usage: <docsetname>

    Parses links from all docs in the specified docset.
    """
    from freequery.client.client import Spec
    spec = Spec(spec)
    program.fqclient(spec).linkparse(**program.option_dict)

@FreequeryDocset.command
def split(program, k, dump):
    """Usage: <k> <dump>

    Splits the dumpfile `dump` into separate files, each with at most `k` documents.
    """
    from freequery.repository.formats import WARCParser, WARCWriter
    if not os.path.isfile(dump):
        print "fq-docset: cannot access '%s': no such dump" % dump
        exit(1)
    try:
        k = int(k)
    except ValueError:
        print "fq-docset: must provide positive integer `k`"
        exit(1)
    if k < 1:
        print "fq-docset: must provide positive integer `k`"
        exit(1)
        
    outfile_name = lambda i: os.path.join(os.path.dirname(dump), "%s-%04d" % (os.path.basename(dump), i))
    outfile_i = 0
    outfile = open(outfile_name(outfile_i), 'w+b')
    writer = WARCWriter(outfile)
    outfile_docs = 0
    with open(dump, 'rb') as infile:
        for doc in WARCParser(infile):
            if outfile_docs >= k:
                outfile.close()
                outfile_docs = 0
                outfile_i += 1
                outfile = open(outfile_name(outfile_i), 'w+b')
                writer = WARCWriter(outfile)
            writer.write(doc)
            outfile_docs += 1

if __name__ == '__main__':
    FreequeryDocset(option_parser=FreequeryDocsetOptionParser()).main()
