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

from Bio import SeqIO
from HTSeq import SAM_Reader

class SingleAlign(object):
    """
    here each reference chrom strand is 
    U00096 and not U00096.2
    """ 
    
class SingleContig(object):

class SingleChrom(object):
    """
    here each reference chrom strand is 
    U00096 and not U00096.2
    
    use embl.name not embl.id
    """
    def __init__(self, embl_rec):
        self.embl_rec = embl_rec

def main(args):
    embl_file = None
    sam_file = None
    read_len = None
    kmer = None
    try:
        opts, args = getopt.getopt(args, '', ["embl=", "sam=",
                                              "read-len=", "kmer="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--read-len":
            read_len = int(arg)
        if opt == "--embl":
            embl_file = arg
        if opt == "--sam":
            sam_file = arg
        if opt == "--kmer":
            kmer = int(arg)
    if (not embl_file
        or not read_len
        or not kmer
        or not sam_file):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    d_max = read_len - kmer + 1

if __name__ == '__main__':
    main(sys.argv[1:])
