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
from random import randint

def sim_single_one_contig_prob(L, N, d_max, read_len, precision):
    sim_runs = int(2.1910133173369407 / precision ** 2) + 1
    one_contig = 0
    for r in xrange(sim_runs):
        nuc_seq = [0] * (L - read_len + 1)
        for n in xrange(N):
            nuc_seq[randint(0, L - read_len)] += 1
        
        def single_one_contig():
            prev = None
            for cur in xrange(L - read_len + 1):
                if nuc_seq[cur] != 0:
                    if prev != None:
                        if cur - prev > d_max:
                            return False
                    prev = cur
            return True
        
        if single_one_contig():
            one_contig += 1
                    
    return one_contig / sim_runs

def main(args):
    read_len, L, d_max, N = None, None, None, None
    precision = None  # precision in probability simulation for "95% confidence interval"
    try:
        opts, args = getopt.getopt(args, 'l:r:d:p:n:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-n':
            N = int(arg)
        if opt == '-l':
            L = int(arg)
        if opt == '-r':
            read_len = int(arg)
        if opt == '-d':
            d_max = int(arg)
        if opt == '-p':
            precision = float(arg)
    if read_len == None or L == None or d_max == None or precision == None or N == None:
        print >> sys.stderr, "missing"
        sys.exit(1)
    print sim_single_one_contig_prob(L, N, d_max, read_len, precision)
    
if __name__ == '__main__':
    main(sys.argv[1:])    

