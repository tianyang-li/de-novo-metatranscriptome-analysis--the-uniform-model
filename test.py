#!/usr/bin/env python

#  Copyright (C) 2012 Tianyang Li
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

import sys
import getopt

import metatranscirptome_uniform_de_novo as uni

def main(args):
    bowtie2, contigs, read_len, kmer = None, None, None, None
    try:
        opts, args = getopt.getopt(args, 'b:c:l:k:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == 'b':
            # bowtie2 SAM file
            bowtie2 = arg
        if opt == 'c':
            # FASTA file containing contigs
            contigs = arg
        if opt == '-l':
            read_len = int(arg)
        if opt == 'k':
            kmer = int(arg)
    if bowtie2 == None or contigs == None or read_len == None or kmer == None:
        print >> sys.stderr, "Missing options"
        sys.exit(2)
    
if __name__ == '__main__':
    main(sys.argv[1:])


