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

from __future__ import division

import getopt
import sys

from HTSeq import SAM_Reader
from Bio import SeqIO

from math import log

from single_one_contig_0 import find_one_contig_N

def single_est_len(l, n, read_len):
    

class SingleOneContig(object):
    def __init__(self, d_max, read_len):
        self.MAX_LEN = 6000
        self.N = find_one_contig_N(0.01, 0.95, self.MAX_LEN, d_max, read_len)
        self.d_max = d_max
        self.read_len = read_len
    
    def __call__(self, l, n):
        if (n / (l - self.read_len + 2 * self.d_max + 1) 
            > self.N / (self.MAX_LEN - self.read_len + 1)):
            return True
        return False

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
        
    contigs = {}
    for rec in SeqIO.parse(assembled_file, 'fasta'):
        # length, read_count
        contigs[rec.name] = [len(rec.seq), 0]
    for align in SAM_Reader(sam_file):
        if align.aligned:
            if align.iv.chrom in contigs:
                contigs[align.iv.chrom][1] += 1
                
    d_max = read_len - assembly_kmer + 1  # max difference between 2 read starting positions
    keep_contig = SingleOneContig(d_max)
    
    for contig, contig_stat in contigs.iteritems():
        if contig_stat[1] != 0:
            if keep_contig(contig_stat[0], contig_stat[1]):
                # name, length, read_count, est_len
                print contig, contig_stat[0], contig_stat[1], single_est_len(contig_stat[0], contig_stat[1])
    
if __name__ == '__main__':
    main(sys.argv[1:])    

