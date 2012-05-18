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
from itertools import izip
from Bio import SeqIO

def main(args):
    fin1, fin2 = None, None
    prefix, tag = None, None
    fmt = None
    try:
        opts, args = getopt.getopt(args, '1:2:p:f:t:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-1':
            fin1 = arg
        if opt == '-2':
            fin2 = arg
        if opt == '-p':
            # prefix for read ID
            prefix = arg
        if opt == '-t':
            # prefix for output file
            tag = arg
        if opt == '-f':
            fmt = arg
    if fin1 == None or fin2 == None or prefix == None or tag == None or fmt == None:
        print >> sys.stderr, "missing"
        sys.exit(1)
    read_count = 0
    with open("%s_1.%s" % (tag, fmt), 'w') as fout1:
        with open("%s_2.%s" % (tag, fmt), 'w') as fout2:
            for rec1, rec2 in izip(SeqIO.parse(fin1, fmt), SeqIO.parse(fin2, fmt)):
                rec1.id = "%s.%d/1" % (prefix, read_count)
                rec2.id = "%s.%d/2" % (prefix, read_count)
                fout1.write(rec1.format(fmt))
                fout2.write(rec2.format(fmt))
                read_count += 1

if __name__ == '__main__':
    main(sys.argv[1:])    
    
