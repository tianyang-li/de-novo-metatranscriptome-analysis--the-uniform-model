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

from __future__ import division
import getopt
import sys
import random

from mle_1 import est

def main(args):
    L, N, runs, d_max, bound = None, None, None, None, None
    try:
        opts, args = getopt.getopt(args, 'L:N:r:d:b:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-L':
            L = int(arg)
        if opt == '-N':
            N = int(arg)
        if opt == '-r':
            # number of runs when generating contigs
            runs = int(arg)    
        if opt == '-d':
            d_max = int(arg)
        if opt == '-b':
            bound = float(arg)
    if L == None or N == None or runs == None or d_max == None or bound == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    random.seed()
    
    for r in xrange(runs):
        start_pos = L * [0]
        for each_read in xrange(N):
            start_pos[random.randint(0, L - 1)] += 1
        prev_pos = None
        c, n = 0, 0
        for read_pos in xrange(len(start_pos)):
            if start_pos[read_pos] > 0:
                if prev_pos != None:
                    if read_pos - prev_pos > d_max:
                        if n >= 3:
                            L_est, N_est, lh = est(c, n, d_max)
                            if c / L_est >= bound and n / N_est >= bound:
                                print L_est, N_est
                            c, n = 0, start_pos[read_pos]
                    else:
                        c += read_pos - prev_pos
                        n += start_pos[read_pos]
                else:
                    n = start_pos[read_pos]
                prev_pos = read_pos
        if n != 0:
            if n >= 3:
                L_est, N_est, lh = est(c, n, d_max)
                if c / L_est >= bound and n / N_est >= bound:
                    print L_est, N_est
        
if __name__ == '__main__':
    main(sys.argv[1:])

