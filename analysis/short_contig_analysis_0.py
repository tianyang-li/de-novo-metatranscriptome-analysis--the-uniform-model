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

import rpy2

from Bio import SeqIO
from HTSeq import SAM_Reader

from single_len_est_0 import single_est_len
from verify_embl_0 import get_embl_feature_intervals, interval_search

class SingleContigAlign(object):
    def __init__(self, contig_len, read_len):
        self.contig_len = contig_len
        self.n_reads = None
    
    def len_est(self, read_len):
        return single_est_len(self.contig_len, self.n_reads, read_len)

def main(args):
    sam_file = None
    embl_file = None
    est_lower_ratio = None
    est_upper_ratio = None
    est_lower_bp = None
    est_upper_bp = None
    blat_blast8_file = None
    read_len = None
    kmer = None
    try:
        opts, args = getopt.getopt(args, '',
                                   ["sam=", "embl=", "contigs=",
                                    "est-lower=", "est-upper="
                                    , "blat-blast8="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--sam":
            # reads onto contig
            sam_file = arg
        if opt == "--embl":
            embl_file = arg
        if opt == "--est-lower":
            est_lower_bp = int(arg.split(",")[1])
            est_lower_ratio = float(arg.split(",")[0])
        if opt == "--est-upper":
            est_upper_bp = int(arg.split(",")[1])
            est_upper_ratio = float(arg.split(",")[0])
        if opt == "--blat-blast8":
            # 0 Query id
            # 1 Subject id
            # 2 % identity
            # 3 alignment length
            # 4 mismatches
            # 5 gap openings
            # 6 q. start
            # 7 q. end
            # 8 s. start
            # 9 s. end
            # 10 e-value
            # 11 bit score
            blat_blast8_file = arg
    if (not sam_file or not embl_file
        or not est_lower_ratio or not est_upper_ratio
        or not est_lower_bp or not est_upper_bp
        or not read_len or not kmer
        or not blat_blast8_file):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    _, features = get_embl_feature_intervals([embl_file])
    

if __name__ == '__main__':
    main(sys.argv[1:])


