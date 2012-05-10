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

import csv

import rpy2

from Bio import SeqIO
from HTSeq import SAM_Reader

from single_len_est_0 import single_est_len
from verify_embl_0 import get_embl_feature_intervals, interval_search, Interval

class AnnotationIntervals(object):
    def __init__(self):
        #      [ .. q .. ]
        #   [ .... s .... ]
        self.q_in_s = []
        #     [ ..... q .... ]
        #           [ .... s .......]
        # or the other side
        self.q_overlaps_s = []
        #  [ ......... q ............ ]
        #       [ ....  s ..... ]
        self.q_covers_s = []

class SingleContigAlign(object):
    def __init__(self, contig_len, read_len):
        self.contig_len = contig_len
        self.n_reads = 0
        self.read_start = [0] * contig_len
        self.annot_ivs = AnnotationIntervals()
    
    def len_est(self, read_len):
        return single_est_len(self.contig_len, self.n_reads, read_len)
    
    def check_contig(self, read_len):
        if self.read_start[0] == 0:
            return False
        for pos in xrange(1, read_len):
            if self.read_start[-pos] != 0:
                return False
        return True 

def get_contigs_info(contigs_file, read_len, sam_file):
    contigs = {}
    for rec in SeqIO.parse(contigs_file, 'fasta'):
        contigs[rec.id] = SingleContigAlign(len(rec.seq), read_len)
    for align in SAM_Reader(sam_file):
        if align.aligned and align.iv.chrom in contigs:
            contig = contigs[align.iv.chrom]
            contig.read_start[align.iv.start] += 1
            contig.n_reads += 1
    return contigs

def search_contigs_ref_ivs(contigs, blat_blast8_file, align_identity, e_val, features):
    with open(blat_blast8_file, 'r') as blat_blast8:
        reader = csv.reader(blat_blast8, delimiter="\t")
        for row in reader:
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
            #
            # positions: one based inclusive
            if (float(row[2]) / 100 > align_identity 
                and row[10] < e_val):
                s_iv = Interval(int(row[8]) - 1, int(row[9]))
                annot_iv = interval_search(features[row[1].split("|")[-1]], s_iv)
                if annot_iv:
                    
                # TODO: 

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
    contigs_file = None
    align_identity = None
    e_val = None
    try:
        opts, args = getopt.getopt(args, '',
                                   ["sam=", "embl=", "contigs=",
                                    "est-lower=", "est-upper="
                                    , "blat-blast8=", "contig-align-identity=",
                                    "read-len=", "kmer=", "e-value="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--read-len":
            read_len = int(arg)
        if opt == "--kmer":
            kmer = int(arg)
        if opt == "--contigs":
            contigs_file = arg
        if opt == "--contig-align-identity":
            # percentage converted to decimal
            align_identity = float(arg)
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
        if opt == "--e-value":
            e_val = float(arg)
    if (not sam_file or not embl_file
        or not est_lower_ratio or not est_upper_ratio
        or not est_lower_bp or not est_upper_bp
        or not read_len or not kmer
        or not align_identity
        or not contigs_file
        or not e_val
        or not blat_blast8_file):
        print >> sys.stderr, "missing"
        print (sam_file, embl_file, est_lower_bp
               , est_lower_ratio, est_upper_bp, est_upper_ratio
               , read_len, kmer, align_identity, contigs_file, blat_blast8_file)
        sys.exit(1)
    
    _, features = get_embl_feature_intervals([embl_file])
    contigs = get_contigs_info(contigs_file, read_len, sam_file)
    search_contigs_ref_ivs(contigs, blat_blast8_file, align_identity, e_val, features)
    
if __name__ == '__main__':
    main(sys.argv[1:])


