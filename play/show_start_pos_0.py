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

from Bio import SeqIO
from HTSeq import SAM_Reader

def show_start_pos(contigs_file, sam):
    contigs = {}
    for rec in SeqIO.parse(contigs_file, 'fasta'):
        contigs[rec.id] = str(rec.seq)
    
def main(args):
    contigs, sam = None, None
    try:
        opts, args = getopt.getopt(args, '', ["contigs=", "sam="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--contigs":
            contigs = arg
        if opt == "--sam":
            sam = arg
    if not contigs or not sam:
        print >> sys.stderr, "missing"
        sys.exit(1)
        
    show_start_pos(contigs, sam)

if __name__ == '__main__':
    main(sys.argv[1:])
