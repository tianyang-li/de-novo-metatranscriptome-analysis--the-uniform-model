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
import random

from mle_1 import est

def rand_contigs(L, N, d):
    seq_reads = L * [0]
    for i in xrange(N):
        seq_reads[random.randint(0, L - 1)] += 1

def main(args):
    c, n, bs_runs, d = None, None, None, None
    try:
        opts, args = getopt.getopt(args, 'c:n:b:d:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-c':
            c = int(arg)
        if opt == '-n':
            n = int(arg)
        if opt == '-d':
            d = int(arg)
        if opt == '-b':
            bs_runs = int(arg)
    if c == None or n == None or bs_runs == None or d == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    random.seed()
    
if __name__ == '__main__':
    main(sys.argv[1:])

    


