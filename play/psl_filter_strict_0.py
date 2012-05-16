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
filter out reads (paired) that 
have perfect alignment and no gap

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
    psl1_file = None
    psl2_file = None
    read_len = None
    id_prefix = None
    try:
        opts, args = getopt.getopt(args, '', ["psl1=", "id-prefix=",
                                              "psl2=", "read-len="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--id-prefix":
            id_prefix = arg
        if opt == "--psl1":
            psl1_file = arg
        if opt == "--psl2":
            psl2_file = arg
        if opt == "--read-len":
            read_len = int(arg)
    if (not psl1_file
        or not psl2_file
        or not id_prefix
        or not read_len):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    good_id1 = set([])
    good_id2 = set([])
    
    with open(psl1_file, 'r') as psl1:
        with open(psl2_file, 'r') as psl2:
            reader1 = csv.reader(psl1, delimiter="\t")
            reader2 = csv.reader(psl2, delimiter="\t")
            for row1, row2 in izip(reader1, reader2):
                block_count_1 = int(row1[17])
                block_count_2 = int(row2[17])
                if block_count_1 == 1 and block_count_2 == 1:
                    if (int(row1[18].split(",")[0]) == read_len and
                        int(row2[18].split(",")[0]) == read_len):
                        good_id1.add(row1[9])
                        good_id2.add(row2[9])
                        
    fout_id1 = open("%s_1.ids" % id_prefix, 'w')
    fout_id2 = open("%s_2.ids" % id_prefix, 'w')
    
    for read_id in good_id1:
        fout_id1.write("%s\n" % read_id)
    for read_id in good_id2:
        fout_id2.write("%s\n" % read_id)                        
    
    fout_id1.close()
    fout_id2.close()
              

if __name__ == '__main__':
    main(sys.argv[1:])
