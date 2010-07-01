#!/usr/bin/env python

import os, sys

from clx import OptionParser, Program

class FreequeryWebsetOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

class FreequeryWebset(Program):
    @property
    def option_dict(self):
        return dict((k, v) for k, v in self.options.__dict__.iteritems()
                           if v is not None)

    def default(self, program, *args):
        ls(program)

@FreequeryWebset.command
def ls(program):
    """Usage:

    Prints the names of all websets.
    """
    pass
    
@FreequeryWebset.command
def new(program, websetname):
    """Usage: <websetname>

    Creates a new webset named `websetname`.
    """
    pass

@FreequeryWebset.command
def rm(program, websetname):
    """Usage: <websetname>

    Deletes the specified webset.
    """
    pass

@FreequeryWebset.command
def add(program, websetname, dump):
    """Usage: <websetname> <dump>

    Adds the dumpfile `dump` to the specified webset.
    """
    pass

@FreequeryWebset.command
def info(program, websetname):
    """Usage: <websetname>

    Prints info about the specified webset.
    """
    pass

if __name__ == '__main__':
    FreequeryWebset(option_parser=FreequeryWebsetOptionParser()).main()
