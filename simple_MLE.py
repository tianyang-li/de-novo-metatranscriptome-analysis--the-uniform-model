#!/usr/bin/env python
from contigs_sam_anal import read_len

# This file is part of de_novo_uniform_metatranscriptome.
# 
# de_novo_uniform_metatranscriptome is free software: 
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# de_novo_uniform_metatranscriptome is distributed in 
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with de_novo_uniform_metatranscriptome.  
# If not, see <http://www.gnu.org/licenses/>.

# Copyright (2012) Tianyang Li
# tmy1018@gmail.com

"""
A simple MLE for estimating transcript length, expression level, etc. in 
metatranscriptome analysis. 

Only contigs that are considered to be the only one contig from the transcript 
that it came from are in the output.
"""

import sys
import getopt
from HTSeq import SAM_Reader
from Bio import SeqIO
import random

def print_usage():
    print >> sys.stderr, "Usage:"
    
def est():
    #TODO
    SINGLE_CONTIG_RUNS = 24000    

def main(args):
    sam, contigs, read_len, kmer = None, None, None, None
    try:
        opts, args = getopt.getopt(args, 's:c:l:k:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-s':
            sam = arg
        if opt == '-c':
            contigs = arg
        if opt == '-k':
            kmer = int(arg)
        if opt == '-l':
            read_len = int(arg)
    if sam == None or contigs == None or read_len == None or kmer == None:
        print_usage()
        sys.exit(1)
    
    # max difference between 2 read starting positions
    # this assumes assembly using de Bruijn graphs
    # overlaps are (k - 1)mers between 2 kmers
    d_max = read_len - kmer + 1
    
    contigs_len = {}
    for rec in SeqIO.parse(contigs, 'fasta'):
        cl = len(str(rec.seq)) - read_len + 1
        if cl > 0:
            # contig length, number of reads on the contig, starting positions of reads
            contigs_len[rec.id] = [len(str(rec.seq)) - read_len + 1, 0, len(str(rec.seq)) - read_len + 1 * [0]]
    
    for aln in SAM_Reader(sam):
        if aln.aligned:
            if aln.iv.chrom in contigs_len:
                contig_rec = contigs_len[aln.iv.chrom]
                if aln.iv.start < contig_rec[0]:
                    contig_rec[1] += 1
                    contig_rec[2][aln.iv.start] += 1
    
    # TODO: estimation
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
        

