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

import getopt
import sys
from math import exp
from numpy.random import poisson

def poisson_rand_contig(lam, d):
    c = 0
    n = 0
    cur_d = 1
    while cur_d <= d:
        cur_reads = poisson(lam)
        if cur_reads > 0:
            n += cur_reads
            c += cur_d
            cur_d = 1
        else:
            cur_d += 1
    return (c, n)

def main(args):
    runs = None
    lam = None
    d = None
    try:
        opts, args = getopt.getopt(args, 'l:d:r:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            lam = float(arg)
        if opt == '-d':
            d = int(arg)
        if opt == '-r':
            runs = int(arg)
    if runs == None or lam == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    for r in xrange(runs):
        c, n = poisson_rand_contig(lam, d)
        print c, n
    
if __name__ == '__main__':
    main(sys.argv[1:])


