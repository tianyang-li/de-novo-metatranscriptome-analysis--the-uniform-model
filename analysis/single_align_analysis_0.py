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

from single_len_est_0 import single_est_len

from short_contig_analysis_single_0 import single_uniform_contig_pval

from align_analysis_utils_0 import SeqOverlapType, SeqInterval, Chrom

from general_util import median

class SingleContig(SeqInterval):
    def __init__(self, c_reads):
        """
        c_reads is a list that contains all the reads (SeqInterval)
        that form this contig
        """
        self.reads = c_reads
        super(SingleContig, self).__init__(c_reads[0].low,
                                           c_reads[-1].high)
    
    
    def coverage(self, read_len):
        return len(self.reads) * read_len / (self.reads[-1].high 
                                             - self.reads[0].low + 1)
    
    
    def est_len(self, read_len):
        return single_est_len(self.high - self.low + 1,
                              len(self.reads), read_len)
        
    
    def uniform_pval(self, read_len, precision=0.01):
        read_pos = [0] * (self.reads[-1].high - self.reads[0].low + 1)
        for read in self.reads:
            read_pos[read.low - self.reads[0].low] += 1
        return single_uniform_contig_pval(read_pos, len(self.reads),
                                          read_len, precision)
    
    
    def max_coverage(self):
        cur_end = 0
        cur_cover = 1
        max_cover = 1
        for cur_read in self.reads[1:]:
            while self.reads[cur_end].high < cur_read.low:
                cur_cover -= 1
                cur_end += 1
            cur_cover += 1
            if cur_cover > max_cover:
                max_cover = cur_cover
        return max_cover
    
    
    def nuc_coverage(self):
        """
        return a list of the coverage of each nuc in sequence 
        """ 
        nuc_cov = []
        cur_cov = 0
        read_start = 0
        read_end = 0
        for cur_nuc in xrange(self.reads[0].low, self.reads[-1].high):
            while (read_start < len(self.reads) 
                   and cur_nuc == self.reads[read_start].low):
                cur_cov += 1
                read_start += 1
            while (read_end < len(self.reads) 
                   and cur_nuc == self.reads[read_end].high + 1):
                cur_cov -= 1
                read_end += 1
            nuc_cov.append(cur_cov)
        return nuc_cov
        

class SingleChrom(Chrom):
    """
    here each reference chrom strand is 
    U00096 and not U00096.2
    
    embl.name (not embl.id)
    """
    
    def assemble_contigs(self, d_max):
        if not self.aligns:
            return
        self.aligns = sorted(self.aligns, cmp=SeqInterval.interval_cmp)
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
        
        self.contigs = filter(lambda contig: len(contig.reads) >= 3,
                              self.contigs)
        
    
    def __init__(self, embl_rec):
        super(SingleChrom, self).__init__(embl_rec)
        self.aligns = []

            
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
            if (int(row[17]) 
                and int(row[18].split(",")[0]) == read_len):
                chroms[row[13]].aligns.append(SeqInterval(int(row[15]),
                                                          int(row[16]) - 1))
    
    for chrom in chroms.itervalues():
        chrom.assemble_contigs(d_max)
        for contig in chrom.contigs:
            nuc_coverage = contig.nuc_coverage()
            est_len = contig.est_len(read_len)
            
            def format_coverage(n_covs):
                cov_str = ""
                for cur_cov in n_covs:
                    cov_str = "%s%d," % (cov_str, cur_cov)
                cov_str = "[%s]" % cov_str
                return cov_str
            
            cov_str = format_coverage(nuc_coverage)
            
            coverage_median = median(nuc_coverage)
            coverage_max = max(nuc_coverage)
            
            for found_iv in chrom.iv_find_features(contig):
                print contig.low, contig.high - contig.low + 1,
                print est_len, 
                print found_iv.type,
                print found_iv.low, found_iv.high - found_iv.low + 1,
                print coverage_median, coverage_max, cov_str, 
                print SeqOverlapType.overlap_type(contig, found_iv)
                """
                0  contig.low
                1  contig.high - contig.low + 1
                2  est_len
                3  found_iv.type
                4  found_iv.low
                5  found_iv.high - found_iv.low + 1
                6  coverage median
                7  coverage max
                8  coverage list
                9  overlap_type
                """

if __name__ == '__main__':
    main(sys.argv[1:])

