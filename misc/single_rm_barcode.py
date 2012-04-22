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

import sys
import getopt

import rm_barcode
 
def main(args):
    sra = None
    try:
        opts, args = getopt.getopt(args, 'i:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-i':
            sra = arg
    cur_srrs = set([])
    for arg in args:
        cur_srrs.add(arg[:-6])
    if sra == None:
        print >> sys.stderr, "missing options"
    srrs = {}  # srrs[SRR] = (SRX, barcode)    
    with open(sra, 'r') as fin:
        for line in fin:
            entries = line.strip().split(" ")
            if entries[0] in cur_srrs:
                srrs[entries[0]] = (entries[1], entries[2])
    for srr, entries in srrs.items():
        pseudo_args = ["-f", "fastq", "-n", "-b", entries[1], "-o", "%s-nobarc-non.fastq" % entries[0], "%s.fastq" % srr]
        rm_barcode.main(pseudo_args)

if __name__ == '__main__':
    main(sys.argv[1:])

  



