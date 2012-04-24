#!/usr/bin/env python

#  Copyright (C) 2012 Tianyang Li
#  tmy1018@gmail.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License

import sys
import getopt

def frag_ml(l, frag_lens):
    frag_str = "(L - %d)%s" % (frag_lens[0], "".join(map(lambda frag: " * (L - %d)" % frag, frag_lens[1:])))
    print >> sys.stderr, "(L - %d) / (%s)" % (l, frag_str)

def main(args):
    l = None
    try:
        opts, args = getopt.getopt(args, 'l:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            # contig length
            l = int(arg)
    if l == None or len(args) == 0:
        print >> sys.stderr, "missing input"
        sys.exit(1)
    print frag_ml(l, map(lambda arg: int(arg), args))
    

if __name__ == '__main__':
    main(sys.argv[1:])

