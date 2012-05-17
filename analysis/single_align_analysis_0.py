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

from Bio import SeqIO

def interval_cmp(iv1, iv2):
    """
    <0 if iv1 < iv2
    =0 if iv1 == iv2
    >0 if iv1 > iv2
    """
    if iv1.low == iv2.low:
        return iv1.high - iv2.high
    return iv1.low - iv2.low

class SeqInterval(object):
    """
    0 based inclusive
    """
    def __init__(self, low, high):
        self.low = low  # integer
        self.high = high  # integer

    def __hash__(self):
        return hash((self.low, self.high))

    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    def __cmp__(self, other):
        return interval_cmp(self, other)

def FeatureInterval(object, SeqInterval):
    def __init__(self, low, high):
        super(FeatureInterval, self).__init__(low, high)
        self.i_min = low
        self.i_max = high

class SingleContig(object):
    def __init__(self):

class SingleChrom(object):
    """
    here each reference chrom strand is 
    U00096 and not U00096.2
    
    embl.name (not embl.id)
    """
    
    def __init__(self, embl_rec):
        self.get_embl_features(embl_rec)
        
        self.aligns = []
        
    def get_embl_features(self, embl_rec):
        self.features = []
        type_source = "source"
        for feat in embl_rec.features:
            if feat.type != type_source:
                self.features.append(FeatureInterval(feat.location.start.position,
                                                    feat.location.end.position - 1))
        self.features = sorted(set(self.features), cmp=interval_cmp)

def main(args):
    embl_file = None
    psl_file = None
    read_len = None
    kmer = None
    try:
        opts, args = getopt.getopt(args, '', ["embl=", "psl=",
                                              "read-len=", "kmer="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--read-len":
            read_len = int(arg)
        if opt == "--embl":
            embl_file = arg
        if opt == "--psl":
            psl_file = arg
        if opt == "--kmer":
            kmer = int(arg)
    if (not embl_file
        or not read_len
        or not kmer
        or not psl_file):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    d_max = read_len - kmer + 1
    
    chroms = {}
    for embl in SeqIO.parse(embl_file, 'embl'):
        chroms[embl.name] = SingleChrom(embl)

if __name__ == '__main__':
    main(sys.argv[1:])

