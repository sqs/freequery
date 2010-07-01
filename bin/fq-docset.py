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

    def default(self, program, *args):
        ls(program)

@FreequeryDocset.command
def ls(program):
    """Usage:

    Prints the names of all docsets.
    """
    pass
    
@FreequeryDocset.command
def new(program, docsetname):
    """Usage: <docsetname>

    Creates a new docset named `docsetname`.
    """
    pass

@FreequeryDocset.command
def rm(program, docsetname):
    """Usage: <docsetname>

    Deletes the specified docset.
    """
    pass

@FreequeryDocset.command
def add(program, docsetname, dump):
    """Usage: <docsetname> <dump>

    Adds the dumpfile `dump` to the specified docset.
    """
    pass

@FreequeryDocset.command
def info(program, docsetname):
    """Usage: <docsetname>

    Prints info about the specified docset.
    """
    pass

if __name__ == '__main__':
    FreequeryDocset(option_parser=FreequeryDocsetOptionParser()).main()
