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

class Interval(object):
    def __init__(self, low, high, strand):
        self.low = low
        self.high = high
        self.strand = strand
        self.max = None

class VerifyLenEst(object):
    def __init__(self, len_est):
        self.len_est = len_est
        self.len_annotation = None

def interval_cmp(iv1, iv2):
    # iv is a tuple
    # (start, end, strand)
    if iv1.low == iv2.low:
        return iv1.high - iv2.high
    return iv1.low - iv2.low

def interval_overlap(iv1, iv2):
    if iv1.low > iv2.high:
        return False
    if iv1.high < iv2.low:
        return False
    return True

def interval_search(features, iv):
    upper = len(features) 
    lower = 0
    x = int((upper - 1 + lower) / 2)
    while (upper > lower + 1 
           and not interval_overlap(features[x], iv)):
        x_left = int((lower + x - 1) / 2)
        x_right = int((x + upper) / 2)

def feature_intervals_max(features):
    

def main(args):
    len_est = None
    psl_align = None
    match_percent = 0.9
    try:
        opts, args = getopt.getopt(args, 'l:a:m:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            len_est = arg
        if opt == '-a':
            psl_align = arg
        if opt == '-m':
            match_percent = float(arg)
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
                    embl_features.append(Interval(feat.location.start.position,
                                          feat.location.end.position, feat.strand))
                else:
                    embl_features.append(Interval(feat.location.end.position,
                                          feat.location.start.position, feat.strand))
        features[embl.id] = embl_features
    
    for embl in features:
        features[embl] = sorted(set(features[embl]), cmp=interval_cmp)
        feature_intervals_max(features[embl])
    
    len_ests = {}
    with open(len_est, 'r') as le:
        reader = csv.reader(le, delimiter=" ")
        for row in reader:
            len_ests[row[0]] = VerifyLenEst(int(row[3]))
    
    with open(psl_align, 'r') as psl:
        reader = csv.reader(psl, delimiter="\t")
        for row in reader:
            if row[9] in len_ests:
                if int(row[1]) / int(row[10]) < 1 - match_percent:
                    t_name = row[13].split("|")[-1]
                    

if __name__ == '__main__':
    main(sys.argv[1:])

