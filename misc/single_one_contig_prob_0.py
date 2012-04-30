#!/usr/bin/env python

import getopt
import sys
import random

def main(args):
    d_max, read_len = None, None
    prob_max =None
    MAX_LEN = 6000
    try:
        opts, args = getopt.getopt(args, 'd:l:u:')
    except getopt.Get as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt,arg in opts:
        if opt=='-l':
        if opt=='-d':
        if opt=='-u':
    if d_max ==None or read_len==None or prob_max==None:
        print >> sys.stderr, "missing options"
        sys.exit(1)

if __name__ == '__init__':
    main(sys.argv[1:])


