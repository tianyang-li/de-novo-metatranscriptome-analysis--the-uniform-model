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

from align_analysis_utils_0 import SeqInterval

class PairedAlign(object):
    """
    0 based inclusive
    """
    def __init__(self, low1, high1, low2, high2):
        self.read1 = SeqInterval(low1, high1)
        self.read2 = SeqInterval(low2, high2)

def psl_paired_align(psl1_file, psl2_file):
    """
    only consider pefectly aligned pairs
    """
    def build_pair(pair, psl_file):
        with open(psl_file, 'r') as psl:
            for line in psl:
                #TODO:
    
    pair1 = {}
    build_pair(pair1, psl1_file)
    pair2 = {}
    build_pair(pair2, psl2_file)
    #TODO:

def main(args):
    psl1_file = None
    psl2_file = None
    embl_file = None
    try:
        opts, args = getopt.getopt(args, '', ["psl1=", "psl2=", "embl="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--psl1":
            psl1_file = arg
        if opt == "--psl2":
            psl2_file = arg
        if opt == "--embl":
            embl_file = arg
    if (not psl1_file
        or not embl_file
        or not psl2_file):
        print >> sys.stderr, "missing"
        sys.exit(1) 

if __name__ == '__main__':
    main(sys.argv[1:])

