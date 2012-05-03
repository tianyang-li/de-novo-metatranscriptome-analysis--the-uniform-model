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
from math import log

def main(args):
    L, read_len = None, None
    d_lower, d_upper = None, None
    precision = None
    try:
        opts, args = getopt.getopt(args, 'L:r:u:l:p:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-L':
            L = int(arg)
        if opt == '-r':
            read_len = int(arg)
        if opt == '-u':
            d_upper = int(arg)
        if opt == '-l':
            d_lower = int(arg)
        if opt == '-p':
            precision = float(arg)
    if L == None or read_len == None or d_lower == None or d_upper == None or precision == None:
        print >> sys.stderr, "missing"
        sys.exit(1)
    sim_runs = int(2.1910133173369407 / precision ** 2) + 1
    N_lower = 0
    sims = []
    eff_len = L - read_len + 1
    for r in xrange(sim_runs):
        sims.append([0] * eff_len)
    for d in xrange(d_upper, d_lower - 1, -1):
        N_upper = N = int(L * log(L) / d) + 1
        one_contig = 0
        print >> sys.stderr, d, N_upper
        for sim in sims:
            for N in xrange(N_lower, N_upper):
                sim[randint(0, eff_len - 1)] += 1
            
            def single_one_contig():
                prev = None
                for cur in xrange(eff_len):
                    if sim[cur] != 0:
                        if prev != None:
                            if cur - prev > d:
                                return False
                        prev = cur
                return True
            
            if single_one_contig():
                one_contig += 1
        print d, one_contig / sim_runs
        N_lower = N_upper

if __name__ == '__main__':
    main(sys.argv[1:])

