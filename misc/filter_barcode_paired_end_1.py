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
    barcode = None
    bc_f = None
    opts, args = getopt.getopt(args, 'b:B:')
    for opt, arg in opts:
        if opt == '-b':
            barcode = arg.upper()
        if opt == '-B':
            bc_f = arg
    all_reads = 0
    kept = 0
    with open("%s-noN_1.fastq" % args[0][:-8], 'w') as fout1:
        with open("%s-noN_2.fastq" % args[1][:-8], 'w') as fout2:
            for barc, seq1, seq2 in izip(SeqIO.parse(bc_f, 'fastq'), SeqIO.parse(args[0], 'fastq'), SeqIO.parse(args[1], 'fastq')):
                all_reads += 1
                if str(barc.seq).upper() == barcode:
                    if "n" not in str(seq1.seq) and "N" not in str(seq1.seq):
                        if "n" not in str(seq2.seq) and "N" not in str(seq2.seq):
                            kept += 1
                            fout1.write(seq1.format('fastq'))
                            fout2.write(seq2.format('fastq'))
    print >> sys.stderr, "%d of %d kept" % (kept, all_reads)

if __name__ == '__main__':
    main(sys.argv[1:])
