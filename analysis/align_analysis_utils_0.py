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

class SeqOverlapType(object):
    #      [ .. q .. ]
    #   [ .... s .... ]
    Q_IN_S = 1
    
    #     [ ..... q .... ]
    #           [ .... s .......]
    # or the other side
    Q_OVERLAP_S = 2
    
    #  [ ......... q ............ ]
    #       [ ....  s ..... ]
    Q_COVER_S = 3
    
    @staticmethod
    def overlap_type(q_iv, s_iv):
        if q_iv.low >= s_iv.low:
            if q_iv.high <= s_iv.high:
                return SeqOverlapType.Q_IN_S
            
            return SeqOverlapType.Q_OVERLAP_S
        
        if q_iv.high <= s_iv.high:
            return SeqOverlapType.Q_OVERLAP_S
        
        return SeqOverlapType.Q_COVER_S
    

class SeqInterval(object):
    """
    0 based inclusive
    """
    def __init__(self, low, high):
        self.low = low  # integer
        self.high = high  # integer
        

    def __hash__(self):
        return hash((self.low, self.high))
    

    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    
    def __cmp__(self, other):
        return SeqInterval.interval_cmp(self, other)
    
    @staticmethod
    def overlap(iv1, iv2):
        if (iv1.low > iv2.high
            or iv1.high < iv2.low):
            return False
        return True
    
    @staticmethod
    def interval_cmp(iv1, iv2):
        """
        <0 if iv1 < iv2
        =0 if iv1 == iv2
        >0 if iv1 > iv2
        """
        if iv1.low == iv2.low:
            return iv1.high - iv2.high
        return iv1.low - iv2.low
        

class FeatureInterval(SeqInterval):
    def __init__(self, low, high, type):
        super(FeatureInterval, self).__init__(low, high)
        self.i_min = low
        self.i_max = high
        self.type = type

class Chrom(object):
    def __init__(self, embl_rec):
        self._get_embl_features(embl_rec)    
        self.seq_str = str(embl_rec.seq).upper()


    def _get_embl_features(self, embl_rec):
        self.features = []
        bad_features = set(["repeat_region", "rep_origin",
                            "misc_feature",
                            "source", "gap", "mobile_element"])
        for feat in embl_rec.features:
            if feat.type not in bad_features:
                self.features.append(FeatureInterval(feat.location.start.position,
                                                    feat.location.end.position - 1,
                                                    feat.type))
        self.features = sorted(set(self.features), cmp=SeqInterval.interval_cmp)
        self._build_feature_tree()
        
    
    def _build_feature_tree(self):
        def set_min_max(l, h):
            x = int((l + h) / 2)
            if l < x:
                tmp_min, tmp_max = set_min_max(l, x - 1)
                if tmp_min < self.features[x].i_min:
                    self.features[x].i_min = tmp_min
                if tmp_max > self.features[x].i_max:
                    self.features[x].i_max = tmp_max
            if h > x:
                tmp_min, tmp_max = set_min_max(x + 1, h)
                if tmp_min < self.features[x].i_min:
                    self.features[x].i_min = tmp_min
                if tmp_max > self.features[x].i_max:
                    self.features[x].i_max = tmp_max
            return self.features[x].i_min, self.features[x].i_max
        
        set_min_max(0, len(self.features) - 1)
    
    
    def iv_find_features(self, q_iv):
        def find_iv(l, h):
            x = int((l + h) / 2)
            if (self.features[x].i_max < q_iv.low
                or self.features[x].i_min > q_iv.high):
                return []
            if SeqInterval.overlap(self.features[x], q_iv):
                found_ivs = [self.features[x]]
            else:
                found_ivs = []
            if l < x:
                found_ivs.extend(find_iv(l, x - 1))
            if h > x:
                found_ivs.extend(find_iv(x + 1, h))
            return found_ivs
        
        return find_iv(0, len(self.features) - 1)
    
        
    def get_GC(self, iv):
        GC = 0
        for nuc in self.seq_str[iv.low:iv.high + 1]:
            if nuc == "G" or nuc == "C":
                GC += 1
        return GC / (iv.high - iv.low + 1)
    

def operon_analysis(contig, features):
    """
    how to improve analysis by
    taking into account operons in bacteria??? 
    """

