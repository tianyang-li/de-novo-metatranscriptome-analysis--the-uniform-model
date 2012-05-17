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

def interval_cmp(iv1, iv2):
    """
    <0 if iv1 < iv2
    =0 if iv1 == iv2
    >0 if iv1 > iv2
    """
    if iv1.low == iv2.low:
        return iv1.high - iv2.high
    return iv1.low - iv2.low

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
        return interval_cmp(self, other)

class FeatureInterval(SeqInterval):
    def __init__(self, low, high):
        super(FeatureInterval, self).__init__(low, high)
        self.i_min = low
        self.i_max = high

class SingleContig(SeqInterval):
    def __init__(self, c_reads):
        """
        c_reads is a list that contains all the reads (SeqInterval)
        that form this contig
        """
        self.reads = c_reads
        super(SingleContig, self).__init__(c_reads[0].low,
                                           c_reads[-1].high)

class SingleChrom(object):
    """
    here each reference chrom strand is 
    U00096 and not U00096.2
    
    embl.name (not embl.id)
    """
    
    def assemble_contigs(self, d_max):
        if not self.aligns:
            return
        self.aligns = sorted(self.aligns, cmp=interval_cmp)
        self.contigs = []
        cur_contig = [self.aligns[0]]
        prev_align = self.aligns[0]
        for align in self.aligns[1:]:
            if align.low - prev_align.low <= d_max:
                cur_contig.append(align)
            else:
                self.contigs.append(SingleContig(cur_contig))
                cur_contig = [align]
            prev_align = align
        self.contigs.append(SingleContig(cur_contig))
    
    def __init__(self, embl_rec):
        self._get_embl_features(embl_rec)    
        self.aligns = []
        
    def _get_embl_features(self, embl_rec):
        self.features = []
        bad_features = set(["repeat_region", "rep_origin",
                            "misc_feature",
                            "source", "gap", "mobile_element"])
        for feat in embl_rec.features:
            if feat.type not in bad_features:
                self.features.append(FeatureInterval(feat.location.start.position,
                                                    feat.location.end.position - 1))
        self.features = sorted(set(self.features), cmp=interval_cmp)
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

def main(args):
    embl_file = None
    psl_file = None
    read_len = None
    kmer = None
    try:
        opts, args = getopt.getopt(args, '', ["embl=", "psl=",
                                              "read-len=", "kmer="])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--read-len":
            read_len = int(arg)
        if opt == "--embl":
            embl_file = arg
        if opt == "--psl":
            psl_file = arg
        if opt == "--kmer":
            kmer = int(arg)
    if (not embl_file
        or not read_len
        or not kmer
        or not psl_file):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    d_max = read_len - kmer + 1
    
    chroms = {}
    for embl in SeqIO.parse(embl_file, 'embl'):
        chroms[embl.name] = SingleChrom(embl)
        
    with open(psl_file) as psl_in:
        for line in psl_in:
            row = line.strip().split("\t")
            """
            0 matches - Number of bases that match that aren't repeats
            1 misMatches - Number of bases that don't match
            2 repMatches - Number of bases that match but are part of repeats
            3 nCount - Number of 'N' bases
            4 qNumInsert - Number of inserts in query
            5 qBaseInsert - Number of bases inserted in query
            6 tNumInsert - Number of inserts in target
            7 tBaseInsert - Number of bases inserted in target
            8 strand - '+' or '-' for query strand. For translated alignments, 
                second '+'or '-' is for genomic strand
            9 qName - Query sequence name
            10 qSize - Query sequence size
            11 qStart - Alignment start position in query
            12 qEnd - Alignment end position in query
            13 tName - Target sequence name
            14 tSize - Target sequence size
            15 tStart - Alignment start position in target
            16 tEnd - Alignment end position in target
            17 blockCount - Number of blocks in the alignment (a block 
                contains no gaps)
            18 blockSizes - Comma-separated list of sizes of each block
            19 qStarts - Comma-separated list of starting positions of 
                each block in query
            20 tStarts - Comma-separated list of starting positions of 
                each block in target
            """
            if int(row[17]) and int(row[18].split(",")[0]):
                chroms[row[13]].aligns.append(SeqInterval(int(row[15]),
                                                          int(row[16]) - 1))
    
    for chrom in chroms.itervalues():
        chrom.assemble_contigs(d_max)

if __name__ == '__main__':
    main(sys.argv[1:])

