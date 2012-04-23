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

import getopt
import sys
from itertools import izip

from Bio import SeqIO

def main(args):
    fmt = None  # format: FASTA, FASTQ
    try:
        opts, args = getopt.getopt(args, 'f:s:1:2:p:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    single = None
    pair1, pair2 = None, None
    prefix = None
    for opt, arg in opts:
        if opt == '-f':
            fmt = arg
        if opt == '-s':
            single = arg
        if opt == '-1':
            pair1 = arg
        if opt == '-2':
            pair2 = arg
        if opt == '-p':
            # prefix of output file
            prefix = arg
    if fmt == None:
        print >> sys.stderr, "missing format"
        sys.exit(1)
    if prefix == None:
        print >> sys.stderr, "no prefix for output"
        sys.exit(1)
    if single != None:
        all_reads = 0
        no_ns = 0
        with open("%s.fastq" % prefix, 'w') as fout:
            for seq in SeqIO.parse(single, fmt):
                all_reads += 1
                if "N" not in str(seq.seq) and "n" not in str(seq.seq):
                    fout.write(seq.format(fmt))
                    no_ns += 1
        print >> sys.stderr, "%d in %d no N" % (no_ns, all_reads)
    if pair1 != None and pair2 != None:
        all_pairs = 0
        no_ns = 0
        with open("%s_1.fastq" % prefix, 'w') as fout1:
            with open("%s_2.fastq" % prefix, 'w') as fout2:
                for seq1, seq2 in izip(SeqIO.parse(pair1, fmt), SeqIO.parse(pair2, fmt)):
                    all_pairs += 1
                    if "N" not in str(seq1.seq) and "n" not in str(seq1.seq) and "N" not in str(seq2.seq) and "n" not in str(seq2.seq):
                        fout1.write(seq1.format(fmt))
                        fout2.write(seq2.format(fmt))
                        no_ns += 1
        print >> sys.stderr, "%d in %d no N" % (no_ns, all_pairs)
    
if __name__ == '__main__':
    main(sys.argv[1:])    


