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

import filter_barcode_single_1

def main(args):
    opts, args = getopt.getopt(args, 'i:')
    info = None
    for opt, arg in opts:
        if opt == '-i':
            info = arg
    srr_barcodes = {}
    with open(info, 'r') as fin:
        for line in fin:
            entries = line.strip().split(" ")
            srr_barcodes[entries[0]] = entries[2]
    for seq, barcode in izip(args[::2], args[1::2]):
        pseudo_args = ["-b", srr_barcodes[seq[:-8]], "-B", barcode, seq]
        filter_barcode_single_1.main(pseudo_args)

if __name__ == '__main__':
    main(sys.argv[1:])



