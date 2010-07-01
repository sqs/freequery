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

@Freequery.command
def query(program, q):
    """Usage: <query>

    Search the inverted index for docs matching `query`.
    """
    import commands
    print commands.getoutput("discodex query fq %s" % q)    

if __name__ == '__main__':
    Freequery(option_parser=FreequeryOptionParser()).main()
