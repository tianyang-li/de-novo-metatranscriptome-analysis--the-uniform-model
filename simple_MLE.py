#!/usr/bin/env python

# This file is part of de_novo_uniform_metatranscriptome.
# 
# de_novo_uniform_metatranscriptome is free software: 
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# de_novo_uniform_metatranscriptome is distributed in 
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with de_novo_uniform_metatranscriptome.  
# If not, see <http://www.gnu.org/licenses/>.

# Copyright (2012) Tianyang Li
# tmy1018@gmail.com

"""
A simple MLE for estimating transcript length, expression level, etc. in 
metatranscriptome analysis. 

Only contigs that are considered to be the only one contig from the transcript 
that it came from are in the output.
"""

import sys
import getopt
from HTSeq import SAM_Reader
from Bio import SeqIO
import random

def print_usage():
    print >> sys.stderr, "Usage:"
    
def est():
    #TODO
    SIM_RUNS = 24000    

def main(args):
    sam, contigs, read_len, kmer = None, None, None, None
    if sam == None or contigs == None or read_len == None or kmer == None:
        print_usage()
        sys.exit(1)
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
        

