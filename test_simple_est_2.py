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
from math import exp
from numpy import expm1

from random_contig_gen import rand_cont

def approx_contig(c, n, d):
    """
    approximate "random" contig length given the observed coverage
    
    use an underestimate for the coverage
    """
    lam = n / (c + 1 + 2 * d)
    c_exp = exp(lam) * (expm1(d * lam)) / (expm1(lam)) - d
    return c_exp

def main(args):
    L, N, d, r, a = None, None, None, None, None
    try:
        opts, args = getopt.getopt(args, 'L:N:d:r:a:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-L':
            L = int(arg)
        if opt == '-N':
            N = int(arg)
        if opt == '-d':
            d = int(arg)
        if opt == '-r':
            r = int(arg)
        if opt == '-a':
            a = float(arg)
    if L == None or N == None or d == None or r == None or a == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    random.seed()
    
    for run in xrange(r):
        sim_res = rand_cont(L, N, d)
        for c, n in sim_res[1]:
            if c / approx_contig(c, n, d) < a:
                print int(c * (n + 1) / (n - 1)), n
    
if __name__ == '__main__':
    main(sys.argv[1:])


