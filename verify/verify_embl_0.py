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
import csv

from Bio import SeqIO

def interval_cmp(iv1, iv2):
    # iv is a tuple
    # (start, end, strand)
    if iv1[0] == iv2[0]:
        return iv1[1] - iv2[1]
    return iv1[0] - iv2[0]

def interval_overlap(iv1, iv2):
    if iv1[0] > iv2[1]:
        return False
    if iv1[1] < iv2[0]:
        return True
    return True

def main(args):
    len_est = None
    psl_align = None
    try:
        opts, args = getopt.getopt(args, 'l:a:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            len_est = arg
        if opt == '-a':
            psl_align = arg
    if not len_est or not args or not psl_align:
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    embls = []
    for arg in args:
        embls.extend(list(SeqIO.parse(arg, 'embl')))
    
    features = {}
    for embl in embls:
        embl_features = []
        type_source = 'source'  # don't take annotations of the whole sequence
        for feat in embl.features:
            if feat.type != type_source:
                if (feat.location.start.position 
                    < feat.location.end.position):
                    embl_features.append((feat.location.start.position,
                                          feat.location.end.position, feat.strand))
                else:
                    embl_features.append((feat.location.end.position,
                                          feat.location.start.position, feat.strand))
        features[embl.id] = embl_features
    
    for embl in features:
        features[embl] = sorted(set(features[embl]), cmp=interval_cmp)
    
    len_ests = {}
    with open(len_est, 'r') as le:
        reader = csv.reader(le, delimiter=" ")
        for row in reader:
            len_ests[row[0]] = [int(row[1])]
    
    with open(psl_align, 'r') as psl:
        reader = csv.reader(psl, delimiter="\t")

if __name__ == '__main__':
    main(sys.argv[1:])

