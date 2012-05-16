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
print number of gaps and percentage of matches

0 matches - Number of bases that match that aren't repeats
1 misMatches - Number of bases that don't match
2 repMatches - Number of bases that match but are part of repeats
3 nCount - Number of 'N' bases
4 qNumInsert - Number of inserts in query
5 qBaseInsert - Number of bases inserted in query
6 tNumInsert - Number of inserts in target
7 tBaseInsert - Number of bases inserted in target
8 strand - '+' or '-' for query strand. For translated alignments, second '+'or '-' is for genomic strand
9 qName - Query sequence name
10 qSize - Query sequence size
11 qStart - Alignment start position in query
12 qEnd - Alignment end position in query
13 tName - Target sequence name
14 tSize - Target sequence size
15 tStart - Alignment start position in target
16 tEnd - Alignment end position in target
17 blockCount - Number of blocks in the alignment (a block contains no gaps)
18 blockSizes - Comma-separated list of sizes of each block
19 qStarts - Comma-separated list of starting positions of each block in query
20 tStarts - Comma-separated list of starting positions of each block in target
"""

from __future__ import division

import getopt
import sys

from itertools import izip

import csv

def main(args):
    psl_file = None
    read_len = None
    try:
        opts, args = getopt.getopt(args, '', ["psl=", "read-len="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--psl":
            psl_file = arg
        if opt == "--read-len":
            read_len = int(arg)
    if (not psl_file
        or not read_len):
        print >> sys.stderr, "missing"
        sys.exit(1)
    with open(psl_file, 'r') as psl:
        reader = csv.reader(psl, delimiter="\t")
        for row in reader:
            block_count = int(row[17])
            align_len = 0
            for block_size, _ in izip(row[18].split(","), xrange(block_count)):
                align_len += int(block_size)
            print align_len / read_len, block_count  

if __name__ == '__main__':
    main(sys.argv[1:])

