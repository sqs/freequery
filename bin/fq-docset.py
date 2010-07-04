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

@FreequeryDocset.command
def info(program, docsetname):
    """Usage: <docsetname>

    Prints info about the specified docset.
    """
    pass

if __name__ == '__main__':
    FreequeryDocset(option_parser=FreequeryDocsetOptionParser()).main()
