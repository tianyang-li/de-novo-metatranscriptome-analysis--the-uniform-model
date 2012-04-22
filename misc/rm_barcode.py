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

def main(args):
    barcode = None
    fmt = None
    kick_n = False
    fout = None
    try:
        opts, args = getopt.getopt(args, 'b:f:no:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-b':
            barcode = arg.lower()
        if opt == '-f':
            fmt = arg
        if opt == '-n':
            kick_n = True
        if opt == '-o':
            fout = arg
    if fmt == None or barcode == None or fout == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    def rm_right_barcode(rec):
        if str(rec.seq)[-len(barcode):].lower() == barcode:
            return rec[:-len(barcode)]
        else:
            return None
    with open(fout, 'w') as rm_barc:
        if kick_n == True:
            all_reads = 0
            no_ns = 0
            for rec in SeqIO.parse(args[0], fmt):
                all_reads += 1
                if "n" not in str(rec.seq) and "N" not in str(rec.seq):
                    no_barc = rm_right_barcode(rec)
                    if no_barc != None:
                        no_ns += 1
                        rm_barc.write(no_barc.format(fmt))
            print >> sys.stderr, "%d of %d with no N kept, and barcode stripped" % (no_ns, all_reads)
        else:
            all_reads = 0
            kepts = 0
            for rec in SeqIO.parse(args[0], fmt):
                all_reads += 1
                no_barc = rm_right_barcode(rec)
                if no_barc != None:
                    kepts += 1
                    rm_barc.write(no_barc.format(fmt))
            print >> sys.stderr, "%d of %d kept, and barcode stripped" % (kepts, all_reads)
        
if __name__ == '__main__':
    main(sys.argv[1:])

