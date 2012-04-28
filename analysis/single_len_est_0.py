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

"""
calculate estimated length
"""

import getopt
import sys
from HTSeq import SAM_Reader
from Bio import SeqIO

def main(args):
    sam_file, assembled_file = None, None
    read_len, assembly_kmer = None, None
    try:
        opts, args = getopt.getopt(args, 'a:s:l:k:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-a':
            assembled_file = arg
        if opt == '-s':
            sam_file = arg
        if opt == '-l':
            read_len = int(arg)
        if opt == '-k':
            assembly_kmer = int(arg)
    if sam_file == None or assembled_file == None or assembly_kmer == None or read_len == None:
        print >> sys.stderr, "missing input"
        sys.exit(1)
    
if __name__ == '__main__':
    main(sys.argv[1:])    

