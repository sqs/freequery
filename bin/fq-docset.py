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
    def docset(self):
        from freequery.repository.docset import Docset
        return Docset
    
    def default(self, program, *args):
        ls(program)

@FreequeryDocset.command
def ls(program, docsetname=None):
    """Usage: [docsetname]

    Prints the names of all docsets, or of the dumps in the specified docset.
    """
    if docsetname is None:
        docsets = program.ddfs.list('fq:docset:')
        if docsets:
            print "\n".join(docsets)
    else:
        docset = program.docset(docsetname)
        if docset.exists():
            dumps = docset.dump_names()
            if dumps:
                print "\n".join(dumps)
        else:
            print "fq-docset: cannot access `%s': no such docset" % docsetname
            exit(1)

@FreequeryDocset.command
def rm(program, docsetname):
    """Usage: <docsetname>

    Deletes the specified docset.
    """
    docset = program.docset(docsetname)
    if docset.exists():
        program.docset(docsetname).delete()
    else:
        print "fq-docset: cannot remove `%s': no such docset" % docsetname
        exit(1)

@FreequeryDocset.command
def add(program, docsetname, dump):
    """Usage: <docsetname> <dump>

    Adds the dumpfile `dump` to the specified docset.
    """
    docset = program.docset(docsetname)
    dumpname = os.path.basename(dump)
    docset.add_dump(dumpname, dump)

@FreequeryDocset.command
def info(program, docsetname):
    """Usage: <docsetname>

    Prints info about the specified docset.
    """
    pass

if __name__ == '__main__':
    FreequeryDocset(option_parser=FreequeryDocsetOptionParser()).main()
