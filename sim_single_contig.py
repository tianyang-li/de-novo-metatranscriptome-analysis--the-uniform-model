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

from random_contig_gen import rand_cont

def single_contig_prob(L, N, d, runs):
    single_cnt = 0
    for r in xrange(runs):
        sim_res = rand_cont(L, N, d)
        if len(sim_res[1]) == 1:
            single_cnt += 1
    return single_cnt / runs

def main(args):
    L, N, d = None, None, None
    runs = 24000
    try:
        opts, args = getopt.getopt(args, 'L:N:r:d:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-L':
            L = int(arg)
        if opt == '-N':
            N = int(arg)
        if opt == '-r':
            runs = int(arg)
        if opt == '-d':
            d = int(arg)
    if L == None or N == None or d == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    print single_contig_prob(L, N, d, runs)
    
if __name__ == '__main__':
    main(sys.argv[1:])    

