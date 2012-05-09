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

from __future__ import division

import getopt
import sys

from single_len_est_0 import single_est_len
from single_one_contig_0 import find_one_contig_N

def main(args):
    sam_file , contigs_file = None, None
    read_len, kmer = None, None
    try:
        opts, args = getopt.getopt(args, '',
                                   ["--sam=", "--contigs=", "--read-len=", "--kmer="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--sam":
            sam_file = arg
        if opt == '--contigs':
            contigs_file = arg
        if opt == "--read-len":
            read_len = int(arg)
        if opt == "--kmer":
            kmer = int(arg)
    if not sam_file or not contigs_file or not read_len or not kmer:
        print >> sys.stderr, "missing"
        sys.exit(1)
        
    # max difference between 2 read starting positions
    d_max = read_len - kmer + 1  
    
if __name__ == '__main__':
    main(sys.argv[1:])


